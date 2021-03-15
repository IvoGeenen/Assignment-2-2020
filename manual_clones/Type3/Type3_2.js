function baseSnippet() {
    var a = 0;
    var b = 10;

    var i;
    for (i = 0; i < b; i++) {
        if (a < 5) {
            a += 2;
        }
    }
    return a;
}
