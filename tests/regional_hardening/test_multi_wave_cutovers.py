from sports_signal_bot.regional_hardening.contracts import (
    CutoverRehearsalStatus,
    CutoverResidueRecord,
    CutoverRollbackRecord,
    CutoverWaveFamily,
    CutoverWaveRecord,
    MultiWaveCutoverRehearsalFamily,
    MultiWaveCutoverRehearsalParams,
)
from sports_signal_bot.regional_hardening.cutovers import (
    build_multi_wave_cutover_rehearsal,
)


def test_build_multi_wave_cutover():
    waves = [
        CutoverWaveRecord(
            wave_id="w1", family=CutoverWaveFamily.pilot_wave, owner="ops"
        )
    ]
    rollbacks = [CutoverRollbackRecord(rollback_id="r1", path_explicit=True)]
    residues = [CutoverResidueRecord(residue_id="res1", is_visible=True)]

    params = MultiWaveCutoverRehearsalParams(
        family=MultiWaveCutoverRehearsalFamily.two_wave_cutover_rehearsal,
        waves=waves,
        windows=[],
        checkpoints=[],
        rollbacks=rollbacks,
        residues=residues,
    )
    rehearsal = build_multi_wave_cutover_rehearsal(params)

    assert (
        rehearsal.rehearsal_status == CutoverRehearsalStatus.cutover_rehearsed_honestly
    )
