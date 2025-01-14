import re
import periodictable as pt
import sys
# sys.path.append("..") 

class MoleculeMass(object):
	"""docstring for MassVolDen"""
	def __init__(self, ):
		super(MoleculeMass, self).__init__()
		# self.arg = arg

	def unnull(self,num):
		if num==[]:
			num=1
		else:
			num = int(num[0])
		return num  

	def Chem2Element(self,formula):
		'''chemical formula to element and number'''
		# print(formula)
		element = []
		number = []
		formula_sub = re.findall(r'[A-Z][^A-Z]*',formula)
		# print(formula_sub)

		for i in range(len(formula_sub)):
			# print(formula_sub[i])
			num = re.findall(r'\d+',formula_sub[i])
			num = self.unnull(num)
			# print(num)
			number.append(num)
			ele = ''.join(re.findall(r'[A-Za-z]',formula_sub[i]))
			ele = ele.title()
			element.append(ele)
		# print(element,number)

		return element, number

	def MolMass(self,formula):
		'''分子质量，给出分子中各元素的个数，返回单个分子的质量（g）'''
		element, number = self.Chem2Element(formula)
		molmass = 0
		
		for i in range(len(element)):
			try:
				ele_mass = pt.elements.symbol(element[i]).mass
			except:
				print("ERROR: Can't find "+element[i]+" ......checkout......")
				break     
			molmass += ele_mass*number[i]
		# print(formula,"Molecular mass = ",molmass,"g/mol")
		
		return molmass

if __name__ == '__main__':

	# mol_formulas = ["C20H42","C46H50S","C49H78S","C54H65NO2S"]
	# mass_fractions = [38.68,25.97,32.68,2.66]
	m = MoleculeMass()
	mw = m.MolMass("C20H42")
	print(mw)
