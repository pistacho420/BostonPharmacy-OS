import json
import os


class ProgressManager:
    def __init__(self, filepath="progress/progress.json"):
        self.filepath = filepath
        self.data = {
            "nombre": "Melvin",
            "xp": 0,
            "correctas": 0,
            "incorrectas": 0,
            "racha": 0,
            "modulos_completados": [],
            "ptcb_attempts": 0,
            "ptcb_best_score": 0,
            "ptcb_passed": False,
            
            "achievements": [],
            # PTCB TRACKING
            "examenes_ptcb": 0,
            "mejor_score_ptcb": 0,
            "preguntas_ptcb_correctas": 0,
            "preguntas_ptcb_totales": 0,
        }
        self.load()

    def unlock_achievement(self, logro):
        # ensure achievements list exists
        if "achievements" not in self.data:
            self.data["achievements"] = []
        if logro not in self.data["achievements"]:
            self.data["achievements"].append(logro)
            self.save()
            return True
        return False

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as file:
                saved = json.load(file)
            self.data.update(saved)

        if "logros" not in self.data:
            # legacy key compatibility
            self.data["logros"] = []

        if "achievements" not in self.data:
            self.data["achievements"] = []

        if "nivel" not in self.data:
            self.data["nivel"] = self.get_level()

    def save(self):
        folder = os.path.dirname(self.filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add_xp(self, amount):
        self.data["xp"] += amount
        self.save()

    def correct_answer(self, xp=10):
        self.data["correctas"] += 1
        self.data["racha"] += 1
        self.data["xp"] += xp

        self.update_level()

        if self.data["correctas"] == 10:
            self.unlock_achievement("🥇 First Prescription")
        elif self.data["correctas"] == 25:
            self.unlock_achievement("💊 Medication Expert")
        elif self.data["correctas"] == 50:
            self.unlock_achievement("🏆 Pharmacy Rising Star")

        self.save()

    def wrong_answer(self):
        self.data["incorrectas"] += 1
        self.data["racha"] = 0
        self.save()

    def update_stats(self, correct=True, xp_gain=10):
        if correct:
            self.correct_answer(xp_gain)
        else:
            self.wrong_answer()

    def get_level(self):
        xp = self.data["xp"]
        if xp >= 500:
            return "💎 Pharmacy Master"
        elif xp >= 250:
            return "🥇 Advanced Pharmacy Technician"
        elif xp >= 100:
            return "🥈 Intermediate Pharmacy Technician"
        return "🥉 Beginner Pharmacy Technician"

    def update_level(self):
        self.data["nivel"] = self.get_level()
        self.save()

    def complete_module(self, module):
        if module not in self.data["modulos_completados"]:
            self.data["modulos_completados"].append(module)
            self.save()
    def save_ptcb_result(self, score, total):
        self.data["ptcb_attempts"] += 1

        porcentaje = int((score / total) * 100)

        if porcentaje > self.data["ptcb_best_score"]:
            self.data["ptcb_best_score"] = porcentaje

        if porcentaje >= 80:
            self.data["ptcb_passed"] = True

        # 🏅 PTCB ACHIEVEMENTS
        if porcentaje >= 90:
            self.unlock_achievement("🏆 Pharmacy Master")

        if porcentaje >= 80:
            self.unlock_achievement("🎓 PTCB Ready")

        if self.data["ptcb_attempts"] >= 1:
            self.unlock_achievement("📝 PTCB Student")

        self.save()
    # ==========================
    # COMPATIBILITY PROPERTIES
    # ==========================

    @property
    def xp(self):
        return self.data["xp"]

    @xp.setter
    def xp(self, value):
        self.data["xp"] = value

    @property
    def correctas(self):
        return self.data["correctas"]

    @correctas.setter
    def correctas(self, value):
        self.data["correctas"] = value

    @property
    def incorrectas(self):
        return self.data["incorrectas"]

    @incorrectas.setter
    def incorrectas(self, value):
        self.data["incorrectas"] = value

    @property
    def racha(self):
        return self.data["racha"]

    @racha.setter
    def racha(self, value):
        self.data["racha"] = value

    def get_progress_percent(self):
        xp = self.data["xp"]
        porcentaje = int((xp / 500) * 100) if 500 else 0
        if porcentaje > 100:
            porcentaje = 100
        return porcentaje