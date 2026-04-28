"""
Patient Profile Management
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from mlu_utils.helpers import generate_random_string


class SecurePatientProfile:
    """Patient profile data model"""

    def __init__(
        self,
        patient_id: str,
        name: str,
        email: str,
        country: str,
        state: str = None,
        lab_results: Dict = None,
        auth_key: str = None,
        created_at: str = None,
        updated_at: str = None,
    ):
        self.patient_id = patient_id
        self.name = name
        self.email = email
        self.country = country
        self.state = state
        self.lab_results = lab_results or {}
        self.auth_key = auth_key or generate_random_string(34)
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "email": self.email,
            "country": self.country,
            "state": self.state,
            "lab_results": self.lab_results,
            "auth_key": self.auth_key,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "SecurePatientProfile":
        """Create profile from dictionary"""
        return cls(**data)


class SecurePatientProfileManager:
    """Manager for patient profiles"""

    def __init__(self, profiles_file: str = "secure_patient_profiles.json"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "data")
        self.profiles_file = os.path.join(data_dir, profiles_file) 
        self.profiles: Dict[str, SecurePatientProfile] = {}
        self._load_profiles()

    def _load_profiles(self):
        """Load profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r") as f:
                    profile_data = json.load(f)
                    for patient_id, data in profile_data.items():
                        self.profiles[patient_id] = SecurePatientProfile.from_dict(data)
            except Exception as e:
                print(f"Error loading profiles: {str(e)}")

    def _save_profiles(self):
        """Save profiles to file"""
        try:
            profile_data = {
                patient_id: profile.to_dict()
                for patient_id, profile in self.profiles.items()
            }
            with open(self.profiles_file, "w") as f:
                json.dump(profile_data, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {str(e)}")

    def create_profile(self, profile_data: Dict) -> SecurePatientProfile:
        """Create a new patient profile"""
        if "patient_id" not in profile_data:
            profile_data["patient_id"] = str(uuid.uuid4())

        profile = SecurePatientProfile.from_dict(profile_data)
        self.profiles[profile.patient_id] = profile
        self._save_profiles()
        return profile

    def get_profile(self, patient_id: str) -> Optional[SecurePatientProfile]:
        """Get a patient profile by ID"""
        return self.profiles.get(patient_id)

    def get_profile_by_email(self, email: str) -> Optional[SecurePatientProfile]:
        """Get a patient profile by email"""
        for profile in self.profiles.values():
            if profile.email.lower() == email.lower():
                return profile
        return None

    def update_profile(
        self, patient_id: str, updates: Dict
    ) -> Optional[SecurePatientProfile]:
        """Update a patient profile"""
        profile = self.get_profile(patient_id)
        if not profile:
            return None

        profile_dict = profile.to_dict()
        profile_dict.update(updates)
        profile_dict["updated_at"] = datetime.now().isoformat()

        updated_profile = SecurePatientProfile.from_dict(profile_dict)
        self.profiles[patient_id] = updated_profile
        self._save_profiles()
        return updated_profile

    def update_lab_results(self, patient_id: str, lab_results: Dict) -> bool:
        """Update lab results for a patient"""
        profile = self.get_profile(patient_id)
        if not profile:
            return False

        profile.lab_results.update(lab_results)
        profile.updated_at = datetime.now().isoformat()
        self._save_profiles()
        return True


def generate_synthetic_profiles(count: int = 10) -> List[SecurePatientProfile]:
    """Generate synthetic patient profiles for testing"""
    countries = ["USA", "Canada", "Australia", "UK", "Germany"]
    states = {
        "USA": ["California", "Texas", "New York", "Florida", "Washington"],
        "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta"],
        "Australia": ["New South Wales", "Victoria", "Queensland"],
        "UK": ["England", "Scotland", "Wales"],
        "Germany": ["Bavaria", "Berlin", "Hesse"],
    }

    manager = SecurePatientProfileManager()
    created_profiles = []

    for i in range(count):
        patient_id = f"PAT{1+i}"
        name = f"Patient {i+1}"
        email = f"patient{i+1}@example.com"
        country = countries[i % len(countries)]
        state = states[country][i % len(states[country])]

        # Generate lab results
        # Using medically accurate ranges
        lab_results = {
            "cholesterol_ldl": 100 + (i * 10) % 100,  # 100-199 mg/dL
            "cholesterol_hdl": 35 + (i * 3) % 30,     # 35-64 mg/dL
            "iron_levels": 60 + (i * 5) % 50,         # 60-109 μg/dL
            "B12_vitamin_levels": 250 + (i * 30) % 300, # 250-549 pg/mL
            "white_blood_cell_count": 6.5 + (i * 0.5) % 6.0, # 6.5-12.4 K/μL
        }

        # Create profile
        profile_data = {
            "patient_id": patient_id,
            "name": name,
            "email": email,
            "country": country,
            "state": state,
            "lab_results": lab_results,
            "auth_key": generate_random_string(34),
        }

        profile = manager.create_profile(profile_data)
        created_profiles.append(profile)

    return created_profiles


if __name__ == "__main__":
    # Generate synthetic patient profiles for testing
    profiles = generate_synthetic_profiles(10)
    print(f"Generated {len(profiles)} synthetic patient profiles")