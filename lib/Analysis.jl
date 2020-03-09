module Analysis

ENV["GKSwstype"]="nul"
using JuliaDB,GLM,StatsPlots,Dates

function exp_regress(cases)
    aggregate_cases = groupreduce((Confirmed=+,), cases, :ObservationDate, select=:Confirmed)
    case_data = select(aggregate_cases,
                       (:ObservationDate => d -> (d - Date(2020,1,1)).value, :Confirmed => n -> log(2,n)))
    regression = lm(@formula(Confirmed ~ 1 + ObservationDate), case_data)
    (regression,
     plot(select(aggregate_cases,:ObservationDate), [exp2.(select(case_data,:Confirmed)),exp2.(predict(regression,case_data))], legend=:bottomright, label=["data" "regression"],yaxis=:log))
end

function filter_date(s,e,cases)
    filter(:ObservationDate => d -> s <= d <= e,cases)
end

function filter_country(c,cases)
    filter(Symbol("Country/Region") => r -> r == c,cases)
end

function filter_state(postal,fullname,cases)
    filter(Symbol("Province/State") => ps -> length(ps) >= 2 && (occursin(postal,ps) || ps == fullname), cases)
end

function last_n_days(n,cases)
    filter_date(today() - Day(n), today(),cases)
end

function process_day_file(path,day)
    fullpath = path * "/csse_covid_19_data/csse_covid_19_daily_reports/" * day * ".csv"
    raw = loadtable(fullpath)
    date = Date(day,"m-d-y")
    insertcols(select(raw, (:Confirmed,:Deaths,:Recovered,Symbol("Country/Region"),Symbol("Province/State"))), 1, :ObservationDate => repeat([date],length(raw)))
end

function load_csse_data(path)
    fullpath = path * "/csse_covid_19_data/csse_covid_19_daily_reports/"
    function parse_date(dt)
        try
            Date(dt)
        catch
            Date(2020,01,01)
        end
    end
    report_data = [process_day_file(fullpath * file) for file in filter(f -> f[end-2:end] == "csv",readdir(fullpath))]
    dropmissing(reduce(merge, report_data))
end

function add_new_day(path,day,t)
    new_data = process_day_file(path)
    merge(new_data,t)
end

end
