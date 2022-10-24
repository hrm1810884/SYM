f = open('/home/denjo/dialogue-demo/sid/wav-spklist.txt', 'w')
dir = "/home/denjo/dialogue-demo/record_ATR/wav/"
for spk in range(1,5):
    for wav in range(1,21):
        if(wav < 10):
            filename = dir + "s" + str(spk) + "_b0" + str(wav) + ".wav"
        else:
            filename = dir + "s" + str(spk) + "_b" + str(wav) + ".wav"
        f.write(filename+"\t"+str(spk)+"\n")