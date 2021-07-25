# -*- coding: utf-8 -*-

class MetaSingleton(type):
	def __call__(cls, *args, **kwargs):
		if not cls.__dict__.get("_instance"):
			cls._instance = cls.__new__(cls, *args)
			cls._instance.__init__(*args, **kwargs)
		return cls._instance


class Singleton(object):
	__metaclass__ = MetaSingleton

	@classmethod
	def Instance(cls):
		return cls()

	@classmethod
	def CleanInstance(cls):
		cls._instance = None