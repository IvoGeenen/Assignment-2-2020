function differentSnippet() {
    let a = 0;
    let b = 10;
    let z = 1;

    var i;
    for (i = 0; i < b; i++) {
        if (a < 5) {
            a += 2;
            z += 1;
        } else {
            a += 1;
        }
    }
    return a;
}
