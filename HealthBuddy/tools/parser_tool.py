import re

class ParserTool:
    def __init__(self):
        self.tests = {
            "hemoglobin": ["hemoglobin", "hb"],
            "wbc": ["wbc", "white blood cell", "total leukocyte"],
            "platelets": ["platelet", "plt"],
            "bilirubin_total": ["bilirubin"],
            "sgot": ["sgot", "ast"],
            "sgpt": ["sgpt", "alt"],
            "creatinine": ["creatinine"],
            "urea": ["urea"],
            "tsh": ["tsh"],
            "t3": ["t3"],
            "t4": ["t4"],
            "vitamin_d": ["vit d", "vitamin d", "25-oh"],
            "vitamin_b12": ["b12", "vitamin b12"],
            "fbs": ["fasting", "fbs"],
            "ppbs": ["pp", "post prandial"],
            "hba1c": ["hba1c"],
            "fsh": ["fsh"],
            "lh": ["lh"],
            "prolactin": ["prolactin"],
            "amh": ["amh", "anti mullerian"],
        }

    def detect_test(self, line_lower):
        for test, keys in self.tests.items():
            if any(k in line_lower for k in keys):
                return test
        return None

    def extract_numbers(self, line):
        return re.findall(r"[0-9]+\.?[0-9]*", line)

    def detect_unit(self, line_lower):
        m = re.search(r"(g/dl|mg/dl|ng/ml|iu/l|mlu/ml|%|/ul)", line_lower)
        return m.group(1) if m else ""

    def parse_line(self, line):
        line_lower = line.lower()
        test = self.detect_test(line_lower)
        if not test:
            return None, None

        nums = self.extract_numbers(line)
        if len(nums) == 0:
            return None, None

        value = float(nums[0])
        ref_range = None
        if len(nums) >= 3:
            ref_range = f"{nums[1]} - {nums[2]}"

        return test, {
            "value": value,
            "unit": self.detect_unit(line_lower),
            "flag": "Low" if "low" in line_lower else ("High" if "high" in line_lower else ""),
            "reference_range": ref_range
        }

    def parse(self, text):
        structured = {}
        for line in text.split("\n"):
            test, info = self.parse_line(line)
            if test and info:
                structured[test] = info
        return structured

parser_tool = ParserTool()
