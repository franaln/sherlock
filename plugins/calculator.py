# plugins: calculator


math_re = re.compile('^\\(*(-?\\d+([.,]\\d+)?)([*/+-^]\\(*(-?\\d+([.,]\\d+)?)\\)*)+$')

class Calculator(Plugin):

    def __init__(self):
        pass





    def search(self, query):

        if math_re.search(query) is None:
            return None

        query = query.replace(" ", "").replace(",", ".")


        Pid pid;
        int read_fd, write_fd;
        string[] argv = {"bc", "-l"};
        string? solution = null;

        try
        {
          Process.spawn_async_with_pipes (null, argv, null,
                                          SpawnFlags.SEARCH_PATH,
                                          null, out pid, out write_fd, out read_fd);
          UnixInputStream read_stream = new UnixInputStream (read_fd, true);
          DataInputStream bc_output = new DataInputStream (read_stream);

          UnixOutputStream write_stream = new UnixOutputStream (write_fd, true);
          DataOutputStream bc_input = new DataOutputStream (write_stream);

          bc_input.put_string (input + "\n", query.cancellable);
          yield bc_input.close_async (Priority.DEFAULT, query.cancellable);
          solution = yield bc_output.read_line_async (Priority.DEFAULT_IDLE, query.cancellable);

          if (solution != null)
          {
            double d = double.parse (solution);
            Result result = new Result (d, query.query_string);
            ResultSet results = new ResultSet ();
            results.add (result, Match.Score.AVERAGE);
            query.check_cancellable ();
            return results;
          }
        }

      query.check_cancellable ();
      return null;


    private class Result: Object, Match
    {
      // from Match interface
      public string title { get; construct set; }
      public string description { get; set; }
      public string icon_name { get; construct set; }
      public bool has_thumbnail { get; construct set; }
      public string thumbnail_path { get; construct set; }
      public MatchType match_type { get; construct set; }

      public int default_relevancy { get; set; default = 0; }

      public Result (double result, string match_string)
      {
        Object (match_type: MatchType.TEXT,
                title: "%g".printf (result),
                description: "%s = %g".printf (match_string, result),
                has_thumbnail: false, icon_name: "accessories-calculator");
      }
    }


    public async ResultSet? search (Query query) throws SearchError
    {
    }
  }
}
# import re

# # input is a list of tokens (token is a number or operator)
# tokens = raw_input()

# # remove whitespace
# tokens = re.sub('\s+', '', tokens)

# # split by addition/subtraction operators
# tokens = re.split('(-|\+)', tokens)

# # takes in a string of numbers, *s, and /s. returns the result
# def solve_term(tokens):
#     tokens = re.split('(/|\*)', tokens)
#     ret = float(tokens[0])
#     for op, num in zip(tokens[1::2], tokens[2::2]):
#         num = float(num)
#         if op == '*':
#             ret *= num
#         else:
#             ret /= num
#     return ret

# # initialize final result to the first term's value
# result = solve_term(tokens[0])

# # calculate the final result by adding/subtracting terms
# for op, num in zip(tokens[1::2], tokens[2::2]):
#     result +=  solve_term(num) * (1 if op == '+' else -1)

# print result
