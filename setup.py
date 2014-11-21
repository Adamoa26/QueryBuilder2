from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='querybuilder',
	version='1.0.0.dev1',
	description='Build Queries from emails for Bro-Master (In case ElasticSearch crashes) and ElasticSearch on top of Bro.',
	url='https://github.com/Adamoa26/QueryBuilder/',
      	author='Adam Elliott',
      	author_email='adam.elliott@ou.edu',
      	license='MIT',
		#entry_points={
		#	"console_scripts":[
		#		'es-getmac = querybuilder.command_line:esmac','b-getmac = querybuilder.command_line:bromac',
		#	]
		#},
      	packages=['querybuilder'],
	install_requires=['paramiko','setuptools',],
      	zip_safe=False)
