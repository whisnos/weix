import hashlib, base64
import string,random


class UserService():

	@staticmethod
	def genePwd(pwd, salt):
		# m = hashlib.md5()
		# str = "%s-%s" % (base64.encodebytes(pwd.encode('utf-8')), salt)
		# print('str',str)
		# m.update(str.encode('utf-8'))
		new_temp="%s-%s" %(pwd,salt)
		m = hashlib.md5()
		m.update(new_temp.encode('utf-8'))
		my_key = m.hexdigest()
		return my_key

	@staticmethod
	def geneAuthCode(user_info):
		m=hashlib.md5()
		str = "%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
		m.update(str.encode('utf-8'))
		return m.hexdigest()

	@staticmethod
	def geneSalt(length = 16):
		str=[random.choice((string.ascii_letters +string.digits )) for i in range(length) ]
		return ''.join(str)