function baseSnippet() {
    let x = 0;
    let y = 10;

    var i;
    for (i = 0; i < y; i++) {
        if (x < 5) {
            x += 2; // Comment after statement
        } else {
            x += 1;
        }
    }
    return x;
}
