#! /usr/bin/env python

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def shortestEdge(self):
        return min(self.w, self.h)

    def placeRow(self, row):
        """Input is a list of areas"""

        A = sum(row)
        aw = A / self.h
        ah = A / self.w

        cx = self.x
        cy = self.y

        coordinates = []
        if (self.w >= self.h):
            for r in row:
                dy = r / aw
                coordinates.append((cx, cy, cx + aw, cy + dy))
                cy += dy
        else:
            for r in row:
                dx = r / ah
                coordinates.append((cx, cy, cx + dx, cy + ah))
                cx += dx
        
        return coordinates

    def cutArea(self, area):
        """Remove the area from this rectangle, return new rectangle"""
        if self.w >= self.h:
            aw = area / self.h
            nw = self.w - aw
            return Rect(self.x + aw, self.y, nw, self.h)
        else:
            ah = area / self.w
            nh = self.h - ah
            return Rect(self.x, self.y + ah, self.w, nh)
 
def computeSTM((w, h), areas):
    """ Compute a squarified tree map.
    The algorithm comes from "Squarified Treemaps", Mark Bruls, Kees Huizing, and Jarke J. van Wijk.
    (which in my opinion is a confusing paper, so I took some hints from:)
    https://github.com/imranghory/treemap-squared/blob/master/treemap-squarify.js
    """
    return squarify(areas, [], Rect(0,0,w,h), [])

def squarify(children, row, rect, results):
    if not children:
        results += rect.placeRow(row)
        return results

    w = rect.shortestEdge()

    c = children[0]
    if improvesRatio(row, c, w):
        squarify(children[1:], row + [c], rect, results)
    else:
        results += rect.placeRow(row)
        r2 = rect.cutArea(sum(row))
        squarify(children, [], r2, results)

    return results

def improvesRatio(row, nextnode, w):
    # always improves for empty row
    if not row:
        return True

    return worst(row, w) >= worst(row + [nextnode], w)
    

def worst(row, w):
    """Row is list of areas for each element in the row,
    w is the size of the side of the row """
    square = lambda n: n*n
    ss = square(sum(row))
    ww = square(w)
    ma = (ww * max(row)) / ss
    mi = ss / (ww * min(row))

    return max(ma, mi)
