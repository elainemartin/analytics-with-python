import Ein
import numpy as np


a = np.arange(25).reshape(5,5)
print ('a: ')
print a
b = np.arange(5)
print ('\nb: ')
print b

print("\nba,a->b, a,b")
print("Our Ein function:")
ein1 = Ein.calculate('ba,a->b',a,b)
print ein1
print("\nNumpy Einsum result:")
ein1b = np.einsum('ba,a->b',a,b)
print ein1b

print("\nii, a")
print("Our Ein function:")
ein2 = Ein.calculate('ii', a)
print ein2
print("\nNumpy Einsum result:")
ein2b = np.einsum('ii', a)
print ein2b

print("\nii->i, a")
print("Our Ein function:")
print Ein.calculate('ii->i', a)
print("\nNumpy Einsum result:")
print np.einsum('ii->i', a)


e = np.arange(60).reshape(3,4,5)
print ("\ne: ")
print e
f = np.arange(24).reshape(4,3,2)
print ("\nf: ")
print f

print("\nijk,jil->kl, e,f")
print("Our Ein function:")
ein4 = Ein.calculate('ijk,jil->kl', e, f)
print ein4
print("\nNumpy Einsum result:")
ein4b = np.einsum('ijk,jil->kl', e, f)
print ein4b

print("\nxyz->, e")
print("Our Ein function:")
ein5 = Ein.calculate('xyz->', e)
print ein5
print("\nNumpy Einsum result:")
ein5b = np.einsum('xyz->',e)
print ein5b