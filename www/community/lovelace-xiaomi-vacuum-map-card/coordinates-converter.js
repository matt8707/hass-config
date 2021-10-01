export default class CoordinatesConverter {

    constructor(p1, p2, p3) {
        this.ABMatrix = this.conversionMatrixAB(p1, p2, p3);
        this.BAMatrix = this.conversionMatrixBA(p1, p2, p3);
    }

    conversionMatrixAB(p1, p2, p3) {
        const p1p2ax = p1.a.x - p2.a.x;
        const p1p3ax = p1.a.x - p3.a.x;
        const p1p2ay = p1.a.y - p2.a.y;
        const p1p3ay = p1.a.y - p3.a.y;
        const p1p2bx = p1.b.x - p2.b.x;
        const p1p3by = p1.b.y - p3.b.y;
        const p1p3bx = p1.b.x - p3.b.x;
        const p1p2by = p1.b.y - p2.b.y;

        const divAD = p1p2ax * p1p3ay - p1p3ax * p1p2ay;
        const dibBE = p1p2ay * p1p3ax - p1p3ay * p1p2ax;

        const A = (p1p2bx * p1p3ay - p1p3bx * p1p2ay) / divAD;
        const B = (p1p2bx * p1p3ax - p1p3bx * p1p2ax) / dibBE;
        const C = p1.b.x - A * p1.a.x - B * p1.a.y;

        const D = (p1p2by * p1p3ay - p1p3by * p1p2ay) / divAD;
        const E = (p1p2by * p1p3ax - p1p3by * p1p2ax) / dibBE;
        const F = p1.b.y - D * p1.a.x - E * p1.a.y;

        return {A, B, C, D, E, F};
    }

    conversionMatrixBA(p1, p2, p3) {
        const p1p2ax = p1.a.x - p2.a.x;
        const p1p3ax = p1.a.x - p3.a.x;
        const p1p2ay = p1.a.y - p2.a.y;
        const p1p3ay = p1.a.y - p3.a.y;
        const p1p2bx = p1.b.x - p2.b.x;
        const p1p3by = p1.b.y - p3.b.y;
        const p1p3bx = p1.b.x - p3.b.x;
        const p1p2by = p1.b.y - p2.b.y;

        const divAD = p1p2bx * p1p3by - p1p3bx * p1p2by;
        const dibBE = p1p2by * p1p3bx - p1p3by * p1p2bx;

        const A = (p1p2ax * p1p3by - p1p3ax * p1p2by) / divAD;
        const B = (p1p2ax * p1p3bx - p1p3ax * p1p2bx) / dibBE;
        const C = p1.a.x - A * p1.b.x - B * p1.b.y;

        const D = (p1p2ay * p1p3by - p1p3ay * p1p2by) / divAD;
        const E = (p1p2ay * p1p3bx - p1p3ay * p1p2bx) / dibBE;
        const F = p1.a.y - D * p1.b.x - E * p1.b.y;

        return {A, B, C, D, E, F};
    }

    convertAB(x, y) {
        return this.convert(x, y, this.ABMatrix);
    }

    convertBA(x, y) {
        return this.convert(x, y, this.BAMatrix);
    }

    convert(oldX, oldY, matrix) {
        const {A, B, C, D, E, F} = matrix;
        const x = A * oldX + B * oldY + C;
        const y = D * oldX + E * oldY + F;
        return {x, y};
    }
}
