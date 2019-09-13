#coding=UTF-8
import sys 
import csv 
from collections import namedtuple

#做一个基础的Args的类，用于读取和赋值给每个路径。

class Args(object):

	def __init__(self):
		self.args = sys.argv[1:]

	def _read_args(self,option):
		try:
			index = self.args.index(option)
			return self.args[index +1]
		except (ValueError,IndexError):  #避免出现两种错误，索引错误，数值错误
			print ('Parameter Error1')
			exit()

	@property
	def config_path(self):
		return self._read_args('-c')

	@property
	def user_path(self):
		return self._read_args('-d')

	@property
	def export_path(self):
		return self._read_args('-o')

#做一个实例，Args的对应的是命令行参数做初始化，将每个文件路径进行读取和赋值给实例args
args = Args()

#设置一个namedtuple的表格索引

IncomeTaxTable = namedtuple ('IncomeTaxTable',['start','rate','sub'])

#起征税点

INCOME_START = 5000

#这个就是利用namedtuple建立一个检索表格，名字是IncomeTaxTable，然后分别按照顺序进行赋值。
#之后进行查询的时候，就可以简化判断语句。

IncomeTaxTableReal = [
	IncomeTaxTable(80000,  0.45,  15160),
	IncomeTaxTable(55000,  0.35,  7160),
	IncomeTaxTable(35000,  0.30,  4410),
	IncomeTaxTable(25000,  0.25,  2660),
	IncomeTaxTable(12000,  0.2,  1410),
	IncomeTaxTable(3000,  0.1,  210),
	IncomeTaxTable(0,  0.03,  0)
	]
	
#主要社保税率参数，读取，分别赋值，同上面的办法，可以考虑使用语法糖，字典类型的数据，用于检索。

class Config(object):
	
	def __init__(self):
		self.config = self._read_config()  #给实例的变量赋值，这种私有方法的赋值更加灵活，安全，
                                           #所有需要变动的东西在read中进行调整，保持初始化的

	def _read_config(self):
		config = {} #作为字典，来处理，后面就是有key，value，赋初值，等会方法结束的返回值。
		with open(args.config_path) as f:  #打开文件的方式，open方法中路径为第一参数，
			for line in f.readlines():#迭代读取所有行，因为源文件中存储是按照行存储，
#逐行读取会有前后的空格，空字符，录入文件是按照等号录入相应参数的，所以按照等号来分离
				key,value = line.strip().split('=')
#这个是去掉整个选取行的前后空格
				try:              #避免获取的数值有误，不是正确的数值类型，确保数据清洗成功。
					config[key.strip()] = float(value.strip())  #这个是去掉每个具体key和value的空格
				except ValueError :    #数值错误，避免出现不是浮点数值情况，影响后面的计算
					print ("Parameter Error")
					exit()
		return config
	
	def _get_config(self,key):
		try :
			return self.config[key]
		except KeyError :   #关键字错误
			print ("config error")
			exit()
			
	@property
	def xiaxian(self):
		return self._get_config('JiShuL')
		
	@property
	def shangxian(self):
		return self._get_config('JiShuH')
		
	@property
	def sum_rate(self):
		return sum([
			self._get_config('YangLao'),
			self._get_config('YiLiao'),
			self._get_config('ShiYe'),
			self._get_config('GongShang'),
			self._get_config('ShengYu'),
			self._get_config('GongJiJin')
		])

config = Config()

#用户数据，是数组，然后里面是具体的元组数据，可以扩充。

class User(object):
	

	
	def __init__(self) :
		self.userlist = self._read_user()
		
	def _read_user(self) :
		userlist = []	
		with open(args.user_path) as f:
			for line in f.readlines():   #逐行处理，逐行添加到数组当中，并且以一个元素加入，元素内数值顺序就是id和工资
				user_id,user_income_str = line.strip().split(",")
				try :   #确保输入的可以转为整数型，避免后期计算出错。
					user_income = int(user_income_str)
				except ValueError :  #数值错误
					print ("income type error")
					exit()
				userlist.append ((user_id,user_income))	
		return userlist		
	
	def get_userlist(self) :
		return self.userlist
		
#开始进行计算的部分，现在已经将命令行参数进行初始化，已命令行的实例对象已经可以在配置表，用户表中获取，
#只有到最后导出的时候才会用到第三个命令行参数

#读取了配置表文件，进行数据清理，形成了可以查询的字典，方便后续计算可以调用。

#获取了用户初始工资信息，进行数据整理，形成了一个个数组，这样方便后续计算可以调用。

class Calculator(object):
	
	def __init__(self,userdata):
		self.userdata = userdata

#使用类方法，而不是实例方法，
#计算社保金额，社保金额按照起征点的高低，低于最低的按照最低的那个比例进行计算，高于最高的按照最高计算，其他就是按照真实工资作为基数计算
	@classmethod
	def calc_shebao(cls,user_income): #其实每次只有进行一次运算，而不是整个表格运算，也就是逐行处理的
		if user_income<config.xiaxian:
			return config.xiaxian*config.sum_rate
		elif user_income>config.shangxian :
			return config.shangxian * config.sum_rate
		else :
			return user_income * config.sum_rate 
			#只是做出来了社保费用
			
	@classmethod
	def calc_income_remain(cls,user_income):  #其实每次只有进行一次运算，而不是整个表格运算，也就是逐行处理的
		shebao = cls.calc_shebao(user_income) #基于社保费用，来进行下一步所得税计算
		real_income = user_income - shebao
		tax_part = real_income - INCOME_START
		
		for item in IncomeTaxTableReal :
			if tax_part > item.start :  #首先检索表格的使用，它是一个必须是有区间的，才可以进行检索，这种检索方式有点怪
				tax = tax_part * item.rate -item.sub
				return '{:.2f}'.format(tax),'{:.2f}'.format(real_income-tax)
				#到此为止，返回的是税费，还有税后剩余
				#添加到数组数据中的数据，也就是打算导出的数据，是ID，工资，养老费用，税费，税后所得，现在都计算获得了。
				
				#也有可能不在这个检索表格里面的区间范围，比如小于0，这个时候也要返回值，所以这个应该是在if外面的，if外面表示的是为假如何处理
		return '0.00','{:.2f}'.format(real_income)
			
	#所以上面的这两个类方法，其实并不是针对于实例，只要有相应的传入数值，他们就可以进行计算返回结果，他们与实例无关。
	#计算实例，要考虑的就是具体数据的传导。
	def calc_all(self):
		result = []
		for user_id,user_income in self.userdata.get_userlist():
			shebao = '{:.2f}'.format(self.calc_shebao(user_income))
			tax,tax_remain = self.calc_income_remain(user_income)
			result.append([user_id,user_income,shebao,tax,tax_remain])
		return result
		
		
		#每一个函数，都有In，Out 所以必须要进行指明，代入，return的结果，而不是直接调用其他函数的结果。
		
	def export(self):
		result = self.calc_all()
		with open(args.export_path,'w',newline='') as f :  #注意写入数据的写法，并且要小心每次调用其他实例的结果，或者是类对象，都要有指明
			writer = csv.writer(f)
			writer.writerows(result)

if __name__ == '__main__':
	# 创建税后工资计算器
	calculator = Calculator(User())

    # 调用 export 方法导出税后工资到文件
	calculator.export()
	

		
