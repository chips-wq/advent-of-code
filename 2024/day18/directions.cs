
int[] t = new int[]{3, 4, 5};

int[][] dirs = new int[][] {
    new int[]{-1, 0},
    new int[]{0, -1},
    new int[]{1, 0},
    new int[]{0, 1},
};

Queue<int> q = new Queue<int>();
Console.WriteLine($"Queue count = {q.Count}");

foreach(int[] c in dirs) {
    (int dx, int dy) = (c[0], c[1]);
    Console.Write($"dx = {dx}, dy = {dy}\n");
}
