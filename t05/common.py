

class Directory():
    def __init__(self) -> None:
        self.global_depth = 1
        self.buckets = []
        for i in range(2):
             self.buckets.append(Bucket(i))



    def toString(self) -> None:
        print(self.global_depth)
        for i in range(len(self.buckets)):
            self.buckets[i].toString()


class Bucket():
    def __init__(self, bucked_id = int) -> None:
        """Consideraremos o número de slots igual a 4 assim como nos slides"""
        self.local_depth = 1
        self.bucked_id = bucked_id
        self.slots = []

    def toString(self) -> None:
        print(f'\nProfundidade local {self.local_depth} do Bucket {self.bucked_id}')
       
        if len(self.slots) == 0:
            print("Bucket Vazio") 

        for i in range(len(self.slots)):
            print(f'Slot {i+1}/4 do Bucket, valor {self.slots[i]}')
