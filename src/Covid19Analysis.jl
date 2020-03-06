module Covid19Analysis

using Logging, LoggingExtras

function main()
  Base.eval(Main, :(const UserApp = Covid19Analysis))

  include(joinpath("..", "genie.jl"))

  Base.eval(Main, :(const Genie = Covid19Analysis.Genie))
  Base.eval(Main, :(using Genie))
end; main()

end
