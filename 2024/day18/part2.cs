using System.Diagnostics;

const int GRID_SIZE = 70;

int[][] dirs = new int[][] {
    new int[]{-1, 0},
    new int[]{0, -1},
    new int[]{1, 0},
    new int[]{0, 1},
};

run();

/*
 * NOTE:
 *
 * Suppose there after we placed `k` different locations on the grid we can't reach the end.
 *
 * It's clear that placing the `k+1`th one, we will still not be able to reach the grid.
 *
 * Idea: do a binary search for `k` with a bfs.
 *
 * I think this is also related to a MST.
 *
 */


/*
 * Since we are using *Top-Level statements*, we need to drop these at the end here.
 *
 * [return type] [MethodName]([Type parameter1], [Type parameter2]) {
 *  // Method body
 *  return [value];
 * }
*/

bool bfs(int k, List<(int, int)> points) {
    HashSet<(int, int)> p = new HashSet<(int, int)>();
    for (int i = 0; i < k; i++) {
        p.Add(points[i]);
    }

    // Using points[0:k), can I get from (0, 0) to (GRID_SIZE, GRID_SIZE) ?
    Queue<(int, int)> q = new Queue<(int, int)>();
    q.Enqueue((0, 0));

    HashSet<(int, int)> v = new HashSet<(int, int)>();

    while (q.Count != 0) {
        (int x, int y) = q.Dequeue();
        if (v.Contains((x, y))) continue;

        if (x == GRID_SIZE && y == GRID_SIZE) {
            return true;
        }
        v.Add((x, y));
        Debug.Assert(!p.Contains((x,y)));
        
        foreach (int[] D in dirs) {
            (int dx, int dy) = (D[0], D[1]);
            (int r, int c) = (x + dx, y + dy);
            if (r < 0 || r > GRID_SIZE || c < 0 || c > GRID_SIZE) continue;
            if (p.Contains((r, c))) continue;
            q.Enqueue((r, c));
        }
    }

    return false;
}

void run() {
    List<(int x, int y)> points = new List<(int x, int y)>();

    int bytes = 0;
    string? line;
    while ((line = Console.ReadLine()) != null) {
        string[] parts = line.Trim().Split(",");
        (int x, int y) = (int.Parse(parts[0]), int.Parse(parts[1]));
        points.Add((x, y));
        bytes++;
    }
    Debug.Assert(bytes == points.Count);

    Console.Write($"We have {bytes} points in total\n");

    int ans = -1;
    int l = 0, r = bytes;
    while (l <= r) {
        int mid = (r-l)/2 + l;
        // Run bfs with mid and check if it's blocked or not.
        if (bfs(mid, points)) {
            ans = mid;
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    Console.WriteLine($"ans = {ans}");
    Console.WriteLine($"points[ans] = {points[ans]}");
}

