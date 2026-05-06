from sports_signal_bot.regional_hardening.cutovers import build_multi_wave_cutover_rehearsal
from sports_signal_bot.regional_hardening.contracts import (
    MultiWaveCutoverRehearsalFamily, CutoverWaveRecord, CutoverRollbackRecord,
    CutoverResidueRecord, CutoverWaveFamily, CutoverRehearsalStatus
)

def test_build_multi_wave_cutover():
    waves = [CutoverWaveRecord(wave_id="w1", family=CutoverWaveFamily.pilot_wave, owner="ops")]
    rollbacks = [CutoverRollbackRecord(rollback_id="r1", path_explicit=True)]
    residues = [CutoverResidueRecord(residue_id="res1", is_visible=True)]

    rehearsal = build_multi_wave_cutover_rehearsal(
        MultiWaveCutoverRehearsalFamily.two_wave_cutover_rehearsal,
        waves, [], [], rollbacks, residues
    )

    assert rehearsal.rehearsal_status == CutoverRehearsalStatus.cutover_rehearsed_honestly
