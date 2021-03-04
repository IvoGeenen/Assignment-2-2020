function baseSnippet() {
    let a = 0;
    let b = 10;

    var j;
    for (j = 0; j < b; j++) {
        if (a < 5) {
            a += 2;
        } else {
            a += 1;
        }
    }
    return a;
}
