OUT=chall
SRCS=chall.c
LIB=rpmalloc/rpmalloc.*

.PHONY: clean

$(OUT): $(SRCS) 
	gcc $(SRCS) $(LIB) -fstack-protector -o chall

clean:
	rm $(OUT)
