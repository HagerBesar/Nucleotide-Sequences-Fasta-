from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

Builder.load_file('gui.kv')


def fileDic(lines):
    key = []
    value = []
    seq = ''

    for i in lines:
        if '>' in i:
            key.append(i.rstrip('\n'))
            if seq != '': value.append(seq)
            seq = ''
        else:
            seq += i.rstrip('\n')
    value.append(seq)
    seqDictionary = {}
    for i in range(0, len(key)):
        seqDictionary[key[i]] = value[i]

    return [seqDictionary, key]


class Bio(Widget):
    path = ObjectProperty()
    outPut = ObjectProperty()
    record = ObjectProperty()
    seqList = {}
    key = []
    lines = []
    fasta = open('example.fasta', 'r')

    def readFile(self):
        self.lines = []
        self.fasta = open(f'{self.path.text}', 'r')  # open
        if self.fasta.readable():
            self.lines = self.fasta.readlines()
            lines1 = ''.join(self.lines)
            self.outPut.text = str(lines1)
            self.seqList = fileDic(self.lines)[0]  # dic
            self.key = fileDic(self.lines)[1]
            print(self.seqList)
            print(self.key)

    def readByID(self):
        select = self.seqList[f"{self.key[int(self.record.text)]}"]
        self.outPut.text = f">seq{self.record.text} : {str(select)}"

    def showGC(self):
        if self.key[int(self.record.text)] == f">seq{self.record.text}(Done)":
            self.outPut.text = "This Sequence parsed already"
        else:
            DNASeq = self.seqList[f">seq{self.record.text}"]  # id
            outPutGC = [f"Sequence : {DNASeq}"]
            DNASeq = DNASeq.upper()
            Position = DNASeq.find('GC', 0)  # find
            count = 0
            outPutGC.append("Positions :")
            while Position != -1:
                count += 1
                outPutGC.append(f"Position of Donor splice site Candidate at  : {Position}")
                Position = DNASeq.find('GC', Position + 1)

            percent = round(DNASeq.count('GC') / len(DNASeq) * 100)
            outPutGC.append(f"\n We Find ( {count} ) Positions of Donor splice site Candidate = {percent}% ")
            self.outPut.text = '\n'.join(outPutGC)

    def complement(self):
        if self.key[int(self.record.text)] == f">seq{self.record.text}(Done)":
            self.outPut.text = "This Sequence parsed already"
        else:
            DNASeq = self.seqList[f">seq{self.record.text}"]
            com = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}  # dic
            seqList = list(DNASeq)
            output = [f"   Sequence  :  {DNASeq}"]
            a = 0
            for i in DNASeq:
                if i in com:
                    seqList[a] = com[i]
                    a += 1
            dnaComp = ''.join(seqList)  # join
            output.append(f"complement: {dnaComp}")
            output.append(f"\nReverse complement: {dnaComp[::-1]}")
            self.outPut.text = '\n'.join(output)

    def transcription(self):
        if self.key[int(self.record.text)] == f">seq{self.record.text}(Done)":
            self.outPut.text = "This Sequence parsed already"
        else:
            DNASeq = self.seqList[f">seq{self.record.text}"]
            DNASeq = DNASeq.upper()
            output = [f"   Sequence  :  {DNASeq}"]
            RNA = DNASeq.replace('T', 'U')
            output.append(f"\nTranscription :{RNA} ")
            self.outPut.text = '\n'.join(output)

    def save(self):
        if self.key[int(self.record.text)] == f">seq{self.record.text}(Done)":
            self.outPut.text = "This Sequence saved already"
        else:
            fasta = open(f'{self.path.text}', 'w')
            newLines = []
            for i in self.lines:
                if i == f">seq{self.record.text}\n":
                    newLines.append(f">seq{self.record.text}(Done)\n")
                else:
                    newLines.append(i)

            print(newLines)
            if fasta.writable():
                fasta.writelines(newLines)
                fasta.close()
            self.outPut.text = " saved Done"
        self.readFile()


class BioGUI(App):
    def build(self):
        return Bio()


if __name__ == "__main__":
    BioGUI().run()
