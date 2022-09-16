# inc-dec-py
C-style increment and decrement operators for python.
# Q&A:
### q: What
a: this 
```python
#encoding: incdec

i = 6
while i-- != 0:
    print(i)

print(f'eventually {i = }')
```
```console
$ python tester.py
5
4
3
2
1
0
eventually i = -1

```

### q: How
a: Remember the arguments when the walrus operator got merged? Well who's laughing now

Essentially, all it takes is just a little bit of text replacement, from a++ to the most definitely valid py (>=3.8) expression `((a, a := a+1)[0])`. <br />
Which, in a similar fashion to C's ++ operator, increments in place but gets evaluated as it was before the increment. <br />
We achieve this by simply picking out the a from a tuple of itself and itself updated.<br />
Do note that the exact same goes ++a, --a and a-- (just taking either the first or second element corresponding to the operator being prefix or postfix).

### q: But how tf do you do text replacements, i thought python didn't have macros
a: Ahhh, you see, python has the best macros. they're just hidden under the innocent looking encoding scheme. <br />
Ever seen old python codes do stuff like `# -*- coding: utf-8 -*-`? <br />
exactly. So what you can do is just implement a new [codec](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo) with rules of your own, [register](https://docs.python.org/3/library/codecs.html#codecs.register) it to the interpreter, make it run at startup (i'll detail in a bit about placement of the file). This is important if like in the code above, it would usually raise a SyntaxError, so you gotta make it there before the parser.

If you did that, voila, you got yourself whatever text replacement macros your heart desires.

### q: How to run
a: Firstly if you don't know what a python .pth file is, I suggest you read [this](https://docs.python.org/3.10/library/site.html).
basically we want something to run our codec at startup. The way to do that is to:
1. Have the file that defines the codec in site_packages (this could either be in your /lib/python<version>/site_packages or the site_packages of your local virtual env, the latter is probably a better idea).
2. In the same spot, put the .pth files (that all it really contains is an import to your py file).


```console
$ git clone https://github.com/dankeyy/inc-dec-py
$ cp inc-dec-py/incdec.py inc-dec-pyincdec_loader.pth <path-to-site_packages>/
```
And that's it really. Just move those two files to the site_packages of your liking. Now you can make a new file, put the comment `#coding: incdec` on the first or second line, and you should be good to go (of course run with the same interpreter to which's site_packages you added the codec to).

#### credit goes to https://github.com/jonatan1609/codec for the initial idea of messing with codecs like that.
