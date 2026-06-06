import json
import os
from src.detector import ContradictionDetector

def run_evaluation_suite():
    # Load test suite
    test_cases_path = os.path.join("data", "test_cases.json")
    if not os.path.exists(test_cases_path):
        print(f"[Error] Test suite file missing at {test_cases_path}")
        return

    with open(test_cases_path, "r") as f:
        test_cases = json.load(f)

    print("=" * 60)
    print(f"Starting Detector Evaluation Engine (Total: {len(test_cases)} cases)")
    print("=" * 60)

    detector = ContradictionDetector()
    passed_evals = 0

    for idx, case in enumerate(test_cases, 1):
        print(f"\n[Case #{idx}] {case['name']}")
        print(f"Target Expectation: Should Trip = {case['should_trip']}")
        
        # Run detection pipeline
        verdict = detector.analyze_text(case["text"])
        
        # Validate model accuracy against ground truth
        is_correct = (verdict.is_contradictory == case["should_trip"])
        status = "PASSED" if is_correct else "FAILED"
        if is_correct:
            passed_evals += 1

        print(f"Detector Verdict   : Is Contradictory = {verdict.is_contradictory} [{status}]")
        print(f"Diagnostic Reason  : {verdict.reason}")
        print("-" * 40)

    print("\n" + "=" * 60)
    print(f"Final Score: {passed_evals}/{len(test_cases)} cases properly identified.")
    print("=" * 60)

if __name__ == "__main__":
    run_evaluation_suite()