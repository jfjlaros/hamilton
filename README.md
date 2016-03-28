# Hamiltonian path finder

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
