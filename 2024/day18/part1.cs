using System.Diagnostics;

Console.WriteLine("Hello world!");

const int GRID_SIZE = 70;
const int PROCESSED_POINTS = 1024;

int[][] dirs = new int[][] {
    new int[]{-1, 0},
    new int[]{0, -1},
    new int[]{1, 0},
    new int[]{0, 1},
};


/*
 * Reference types: string, class, interface
 * (i'm guessing these are stored on the heap)
 *
 * Value types: int, double, float, bool, char, decimalk
 * (i'm guessing these are stored on the stack)
 *
 * Q: What is a decimal my friends ?
 *
 *
 * (we won't care about this much)
 * unsafe code has pointer types!
 *
 *
 *
 *
 *
 */



/* Tutorial for tuples
(int x, int y) tuple = (9, 1);
Console.WriteLine(tuple.x);


string[] dummy = {"5,3", "9,1"};

for (int i = 0; i < dummy.Length; i++) {
    string[] parts = dummy[i].Split(",");
    (int, int) tt = (int.Parse(parts[0]), int.Parse(parts[1]));
    Console.WriteLine(tt);

    Console.WriteLine();
}
*/

/*
 * How do we do a BFS (like the good old days)
 *
 * 1. initialize a queue
 *
 * 2. add (0, 0) to it
 *
 * 3. extend using a directions array
 *
 */

string? line;

HashSet<(int, int)> set = new HashSet<(int, int)>();

int k = 0;
while ((line = Console.ReadLine()) != null) {
    string[] parts = line.Trim().Split(",");
    (int, int) point = (int.Parse(parts[0]), int.Parse(parts[1]));
    Console.WriteLine(point);
    set.Add(point);
    k++;

    if (k == PROCESSED_POINTS) break;
}

for (int i = 0; i <= GRID_SIZE; i++) {
    for (int j = 0; j <= GRID_SIZE; j++) {
        int x = j, y = i;
        if (set.Contains((x, y))) {
            Console.Write("#");
        } else {
            Console.Write(".");
        }
    }
    Console.WriteLine();
}

Queue<(int, int)> q = new Queue<(int, int)>();
q.Enqueue((0, 0));

HashSet<(int, int)> h = new HashSet<(int, int)>();
Dictionary<(int, int), int> d = new Dictionary<(int, int), int>();
d[(0, 0)] = 0;

while (q.Count != 0) {
    (int x, int y) = q.Dequeue();
    Debug.Assert(d.ContainsKey((x, y)));
    
    foreach (int[] D in dirs) {
        (int dx, int dy) = (D[0], D[1]);
        (int r, int c) = (x + dx, y + dy);

        if (r < 0 || r > GRID_SIZE || c < 0 || c > GRID_SIZE) continue;
        if (set.Contains((r, c))) continue;

        if (d[(x, y)] + 1 < d.GetValueOrDefault((r, c), int.MaxValue)) {
            d[(r, c)] = d[(x, y)] + 1;
            q.Enqueue((r, c));
        }
    }

    Console.WriteLine($"x = {x}, y = {y}");
}

foreach (var (key, value) in d) {
    Console.Write($"key = {key}, value = {value}\n");
}

Console.WriteLine($"ans = {d.GetValueOrDefault((GRID_SIZE, GRID_SIZE))}");
