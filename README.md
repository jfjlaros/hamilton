# Hamiltonian path finder
This library provides functions to find a Hamiltonian path or cycle in a graph
that is induced by a rectangular board and a list of moves.

For a more colourful explanation, see this [notebook](heatmap.ipynb).

```python
>>> import yaml
>>>
>>> from hamilton import Hamilton
>>>
>>> # Load the ruleset from a file and make a new class instance using an
>>> # 8 by 8 board starting at (0, 0).
>>> moves = yaml.load(open('knight.yml'))['moves']
>>> knight = Hamilton(moves, 8, 8, 0, 0)
>>>
>>> # Find a Hamiltonian path.
>>> knight.solve()
True
```

The result is stored in `knight.board` and can be pretty-printed by calling the
`__str__` function.

```python
>>> print knight
  1 26 15 24 29 50 13 32
 16 23 28 51 14 31 64 49
 27  2 25 30 63 60 33 12
 22 17 52 59 44 57 48 61
  3 42 21 56 53 62 11 34
 18 39 54 43 58 45  8 47
 41  4 37 20 55  6 35 10
 38 19 40  5 36  9 46  7

```

The starting position can be altered using the `reset` function.

```python
>>> knight.reset(5, 5)
>>> knight.solve()
True
>>> print knight
 47 64 13 54 27  6 11  8
 14 55 48 61 12  9 26  5
 63 46 57 30 53 28  7 10
 56 15 62 49 60 31  4 25
 45 58 43 52 29 50 21 32
 16 37 40 59 42  1 24  3
 39 44 35 18 51 22 33 20
 36 17 38 41 34 19  2 23

```

Finding a Hamiltonian cycle can be done by passing `closed=True` to the constructor, or by using the `reset` function.

```python
>>> knight.reset(5, 5, closed=True)
>>> knight.solve()
True
>>> print knight
 47 62 13 54 27  6 11  8
 14 55 48 63 12  9 26  5
 61 46 57 30 53 28  7 10
 56 15 60 49 64 31  4 25
 45 58 43 52 29 50 21 32
 16 37 40 59 42  1 24  3
 39 44 35 18 51 22 33 20
 36 17 38 41 34 19  2 23

```

To see how many times backtracking was needed, use the `retries` member
variable.

```python
>>> knight.retries
1
```

## Command line interface
Make a 10 by 10 board and use the rules defined in `metita.yml` to find a
Hamiltonian path starting at position (0, 0).

```bash
$ hamilton metita.yml 10 10 0 0
   1  55  43  16  93  42  70 100  41  35
  58  18   3  57  66   4  39  65   5  38
  44  15  96  54  69  97  94  36  71  99
   2  56  63  17  92  64  67  85  40  34
  59  19  45  77  95  29  80  98   6  37
  52  14  89  53  68  88  91  33  72  86
  23  49  62  28  81  78  27  84  79  10
  60  20  46  76  90  30  73  87   7  32
  51  13  24  50  12  25  82  11  26  83
  22  48  61  21  47  75   8  31  74   9

Number of retries: 0
```

To find a closed path, use the `-c` option.

```bash
$ hamilton -c metita.yml 10 10 0 0
   1  55  43  16  93  42  70  98  41  35
  58  18   3  57  66   4  39  65   5  38
  44  15 100  54  69  99  94  36  71  97
   2  56  63  17  92  64  67  85  40  34
  59  19  45  77  95  29  80  96   6  37
  52  14  89  53  68  88  91  33  72  86
  23  49  62  28  81  78  27  84  79  10
  60  20  46  76  90  30  73  87   7  32
  51  13  24  50  12  25  82  11  26  83
  22  48  61  21  47  75   8  31  74   9

Number of retries: 1
```
