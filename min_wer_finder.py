filename = input("Enter filepath: ")

wers = []

wer_file = open(filename, "r")
for line in wer_file.readlines():
    if line.startswith("%WER"):
        wers.append(float(line.split(" ", maxsplit=3)[1]))

wer_file.close()

print(f"Minimum WER = {min(wers)}")
