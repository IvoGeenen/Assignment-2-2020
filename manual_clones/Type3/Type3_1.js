function baseSnippet() {
    let x = 0;
    let y = 10;
    let z = 1;

    var i;
    for (i = 0; i < y; i++) {
        if (x < 5) {
            x += 2;
            z += 1;
        } else {
            x += 1;
        }
    }
    return x;
}
