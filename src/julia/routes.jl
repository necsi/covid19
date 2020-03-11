using Genie.Router
ENV["GKSwstype"]="nul"
using Analysis,JuliaDB,StatsPlots,GLM

t = Analysis.load_csse_data("public/data")

route("/") do
    print("changed")
    country = @params(:country)
    days = parse(Int,@params(:days))
    chartfilename = "static/$country-$days-chart.png"
    (regress,chart) = Analysis.exp_regress(Analysis.last_n_days(days,Analysis.filter_country(country,t)))
    savefig(chart,"public/$chartfilename")
    "<p>
      In $country, for the last $days days the number of Corona cases has been doubling every $(round(1 / coef(regress)[2],digits=1)) days
    </p>
    <p>
    <img src=\"$chartfilename\"></img>
    </p>"
end
