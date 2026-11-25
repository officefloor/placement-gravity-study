"""Each step script prints the command to run next (README, *Running*)."""

from placement_gravity import nextstep, runs


def test_each_step_names_the_next_with_its_analyses():
    reg = runs.load()
    c = lambda step, **k: nextstep.commands(step, reg, registered=True, **k)
    assert c("2", analyses=["pilot"]) == ["./step3_measure.sh --analysis pilot"]
    assert c("3", analyses=["pilot"]) == ["./step4_analyse.sh --analysis pilot"]
    assert c("3", analyses=["pilot", "open-source-development"]) == [
        "./step3b_histories.sh --analysis open-source-development",
        "./step4_analyse.sh --analysis pilot open-source-development"]
    assert c("2b", samples=["open-source-agent"]) == [
        "./step3b_histories.sh --analysis open-source-agent-within open-source-agent-against-human"]
    assert c("4") == ["./step5_report.sh"] and c("5") == []
    # with no analysis named, every one; the steps then take every one too
    assert c("3") == ["./step4_analyse.sh"]


def test_before_the_tag_the_next_commands_name_the_development_analyses():
    reg = runs.load()
    dev = [a["name"] for a in reg["analyses"] if a["role"] == "development"]
    got = nextstep.commands("1", reg, registered=False)
    assert got[0].startswith("./step1b_timing.sh")      # optional
    got = got[1:]
    assert got[0] == "./step2_runs.sh --analysis " + " ".join(n for n in dev if not nextstep.split(reg, [n])[1])
    assert got[1].startswith("./step2b_samples.sh open-source-development open-source-development-agent")


def test_step_1b_leads_on_to_step_2():
    reg = runs.load()
    assert nextstep.commands("1b", reg, analyses=["pilot"], registered=True) == ["./step2_runs.sh --analysis pilot"]
