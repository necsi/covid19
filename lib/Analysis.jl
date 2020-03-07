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
    filter(Symbol("Province/State") => ps -> length(ps) >= 2 && (ps[end-1:end] == postal || ps == fullname), cases)
end

function last_n_days(n,cases)
    filter_date(today() - Day(n), today(),cases)
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
    function process_day_file(file)
        raw = loadtable(fullpath * file)
        date = Date(file[1:end-4],"m-d-y")
        insertcols(select(raw, (:Confirmed,:Deaths,:Recovered,Symbol("Country/Region"),Symbol("Province/State"))), 1, :ObservationDate => repeat([date],length(raw)))
    end
    report_data = [process_day_file(file) for file in filter(f -> f[end-2:end] == "csv",readdir(fullpath))]
    dropmissing(reduce(merge, report_data))
end

end
