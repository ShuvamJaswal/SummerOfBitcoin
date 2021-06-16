class MempoolTransaction():
	def __init__(self, txid, fee, weight, parents):
		self.txid = txid
		self.fee = int(fee)
		self.weight=int(weight)
		self.parents=parents
	
def parse_mempool_csv():
	with open('mempool.csv') as csv_file:
		next(csv_file) # to skip first line which contains field names
		return(sorted([MempoolTransaction(*line.strip().split(',')) for line in csv_file.readlines()], key= lambda transaction: transaction.fee,reverse=True)) #creating a list of objects of class MempoolTransaction and sorting them in descending order in relation to fee.

def create_block(file_to_write):		
	id_list=[] #temp list to enter IDs of transactions
	totalweight=0 #to store total weight of currently processed transactions.
	for transaction in parse_mempool_csv():
		totalweight+=transaction.weight #increasing current weight per transaction
		if totalweight<=4000000: #checking if block weight is less than 4000000
			if transaction.parents!="": #check if transaction have any parent transactioms
				id_list.extend(transaction.parents.split(";")) #adding parent transaction id to list
			id_list.append(transaction.txid)
		else:
			break #stop loop when maximum supported weight is reached i.e. totalweight>4000000
	for txid in id_list: #writing to block.txt file
			print(txid,file=file_to_write)
#Driver Code			
with open("block.txt","w") as block_file:
				 create_block(block_file)