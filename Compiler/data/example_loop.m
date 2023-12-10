a = 0;
v = [1, 2, 3, 4, 5];

for (i in 1:5) {
    if (v[i] == 4)
        return v[i];
    
    a += i;
}