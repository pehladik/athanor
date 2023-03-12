from pydub import AudioSegment
import json
import argparse
import random



def main(partition, fileout, duration, sounds):
    random.seed(None)

    piste = AudioSegment.silent(duration=duration)

    f = open(partition, "r")
    lines = f.readlines()

    print("start reading partition")
    for idx_line in range(0, len(lines)):
        #print("line:", line, end="")
        line = lines[idx_line]
        res = json.loads(line[line.index("{"):line.index("}")+1])
        pos = int(res['date']*1000)
        
        audiofile =  res['son'][1]+"."+res['son'][0]
        sound = AudioSegment.from_file(sounds+"/"+audiofile, format=res['son'][0])       

        if 'effet' in res.keys():
            effet = res['effet']
            if (effet[0] == "cut"):                
                sound = sound[:int(float(effet[1])*1000)] # cut the sound
            elif (effet[0] == "cut-next"):
                # find next date
                if (idx_line == len(lines) -1):
                    print("attention effet cut-next en fin de partition")
                else:
                    next_line = lines[idx_line+1]
                    n_res = json.loads(next_line[next_line.index("{"):next_line.index("}")+1])
                    sound = sound[:int(float(n_res['date']-res['date'])*1000)] # cut the sound
            elif (effet[0] == "crossfade"): # add crossfade effect
                duration_in = int(float(effet[1])*1000)
                duration_normal = int(float(effet[2])*1000)
                duration_out = int(float(effet[2])*1000)
                
                pos = pos - duration_in
                if (float(effet[1]) > 0):
                    sound = sound.fade(from_gain=-120.0, start=0, duration=duration_in)
                sound = sound.fade(to_gain=-120.0, start=duration_in+duration_normal, duration=duration_out)
                sound = sound[:duration_in + duration_normal + duration_out]
            
            elif (effet[0] == "superposition"): # default behaviour
                pass

        inc = random.choice([True, False])
        if 'canal' in res.keys():
            canal = res['canal']
            #print('canal', canal)
            if (canal[0] == 'stereo') :
                pass
            elif (canal[0] == 'mono-droit') :
                sound = sound.pan(+1.0)
            elif (canal[0] == 'mono-gauche') :
                sound = sound.pan(-1.0)
            elif (canal[0] == 'mono-random') :
                if (random.choice([True, False])):
                    sound = sound.pan(+1.0)
                else:
                    sound = sound.pan(-1.0)
            elif (canal[0] == 'mono-incremental') :
                if (inc):
                    sound = sound.pan(+1.0)
                    inc = False
                else:
                    sound = sound.pan(-1.0)
                    inc = True
            elif (canal[0] == 'circular') :
                duree = canal[2] * 1000                
                circ_sound = AudioSegment.silent(duration=0)
                if (canal[1] == "left_to_right"):
                    sens = 1
                elif (canal[1] == "right_to_left"):
                    sens = -1
                i = 0
                step = 100
                while (i <= duree):
                    circ_sound = circ_sound + sound[i:i+step].pan(sens*(2*i - duree)/duree)
                    i += step
                sound = circ_sound
            elif (canal[0] == 'gain') :
                sound = sound.apply_gain_stereo(int(canal[1]), int(canal[2]))

        piste = piste.overlay(sound, position=pos)

    print("Exporting audio file")
    piste.export(fileout, format="mp3")
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'PyEagle',
                    description = 'Generate a sound file from a partition')
    parser.add_argument("-i", "--partition", help="partition name (with extension)", nargs='?', const='work', default='work')
    parser.add_argument("-s", "--sounds", help="path for sounds repository", nargs='?',default='./sounds')    
    parser.add_argument("-o", "--fileout", help="name of the audio file (with mp3 extension)",  nargs='?',default="mashup.mp3")
    parser.add_argument("-d", "--duration", type=int, help="duration of the audio file (in ms)", nargs='?',default=0)
    args = parser.parse_args()
    main(args.partition, args.fileout, args.duration, args.sounds)

