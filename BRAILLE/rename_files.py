
import subprocess as sp



all_f = sp.check_output("ls numbered_all/").decode("utf-8")
all_f_split = all_f.split("\n")

images = []
annots = []

for i in all_f_split:
    if i[-4:] == ".jpg":
        images.append(i)

    elif i[-4:] == ".xml":
        annots.append(i)


collected = []


count = 1
for i in images:
    for j in annots:
        if i[:10] == j[:10]:
            sp.check_output(f"mv numbered_all/{i} numbered_all/{str(count)}.jpg", shell=True)

            sp.check_output(f"mv numbered_all/{j} numbered_all/{str(count)}.xml", shell=True)
            
            print(count, i, j)
            count += 1
'''
for i, j in zip(images[:], annots[:]):
    collected.append([i])



for j in annots:
    for i in collected:
        if j[]

'''
