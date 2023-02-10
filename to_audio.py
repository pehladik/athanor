from pydub import AudioSegment
import json
import argparse

def main(partition, fileout, duration, sounds):

    piste = AudioSegment.silent(duration=duration)

    f = open(partition, "r")
    lines = f.readlines()

    print("start reading partition")
    for line in lines:
        print("line:", line, end="")
        res = json.loads(line[line.index("{"):line.index("}")+1])
        pos = int(res['date']*1000)
        
        audiofile =  res['son'][1]+"."+res['son'][0]
        sound = AudioSegment.from_file(sounds+"/"+audiofile, format=res['son'][0])       

        if 'effet' in res.keys():
            effet = res['effet']
            if (effet[0] == "cut"):                
                sound = sound[:int(float(effet[1])*1000)] # cut the sound
                print(int(float(effet[1])*1000))
            elif (effet[0] == "crossfade"): # add crossfade effect
                duration_in = int(float(effet[1])*1000)
                duration_normal = int(float(effet[2])*1000)
                duration_out = int(float(effet[2])*1000)
                
                pos = pos - duration_in
                if (effet[1] > 0):
                    sound = sound.fade(from_gain=-120.0, start=0, duration=duration_in)
                sound = sound.fade(to_gain=-120.0, start=duration_in+duration_normal, duration=duration_out)
                sound = sound[:duration_in + duration_normal + duration_out]
            elif (effet[0] == "superposition"): # default behaviour
                pass

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

