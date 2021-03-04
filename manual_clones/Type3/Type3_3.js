function baseSnippet() {
    let x = 0;
    let y = 10;

    var i;
    for (i = 0; i < y; i++) {
        if (x < 5) {
            x *= 3;
        } else {
            x *= 2;
        }
    }
    return x;
}
