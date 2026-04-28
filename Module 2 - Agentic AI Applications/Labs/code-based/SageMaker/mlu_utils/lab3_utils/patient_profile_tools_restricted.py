from .secure_patient_profiles import SecurePatientProfileManager
from strands import tool
import logging
from typing import Dict, Optional, List

# Initialize the restricted patient profile manager
secure_profile_manager = SecurePatientProfileManager()
ALLOWED_PATIENT_KEY = ["tAdlWE7TaMJkOW9zuxQiELcmjmitsvYDpc"]

@tool
def get_patient_profile_restricted(patient_id: str = None, email: str = None) -> Dict:
    """
    Get patient profile information by patient ID or email.
    
    Args:
        patient_id (str, optional): The patient ID to lookup
        email (str, optional): The patient email to lookup
        
    Returns:
        dict: Patient profile information or error message
    """
    
    if not patient_id and not email:
        return {"error": "Either patient_id or email must be provided"}

    try:
        profile = None
        if patient_id:
            profile = secure_profile_manager.get_profile(patient_id)
        elif email:
            profile = secure_profile_manager.get_profile_by_email(email)
            
        if not profile:
            return {"error": "Patient profile not found"}
            
        if profile.auth_key not in ALLOWED_PATIENT_KEY:
            logging.warning(f"Security violation: {patient_id or email}")  # Audit Logging
            return {"error": "You do not have access!"}
            
        return profile.to_dict()
            
    except Exception as e:
        return {"error": "Patient profile not found"}
    
    



@tool
def get_patient_lab_results_restricted(patient_id: str = None, email: str = None) -> Dict:
    """
    Get patient lab results by patient ID or email.
    
    Args:
        patient_id (str, optional): The patient ID to lookup
        email (str, optional): The patient email to lookup
        
    Returns:
        dict: Patient lab results or error message
    """
    
    if not patient_id and not email:
        return {"error": "Either patient_id or email must be provided"}
    
    try:
        profile = None
        if patient_id:
            profile = secure_profile_manager.get_profile(patient_id)
        elif email:
            profile = secure_profile_manager.get_profile_by_email(email)
            
        if not profile:
            return {"error": "Patient profile not found"}
            
        if profile.auth_key not in ALLOWED_PATIENT_KEY:
            logging.warning(f"Security violation: {patient_id or email}")  # Audit Logging
            return {"error": "You do not have access!"}
            
        return profile.lab_results
            
    except Exception as e:
        return {"error": "Patient profile not found"}

@tool
def update_patient_profile_restricted(patient_id: str, updates: Dict) -> Dict:
    """
    Update patient profile information.
    
    Args:
        patient_id (str): The patient ID to update
        updates (dict): The updates to apply to the profile
        
    Returns:
        dict: Updated patient profile or error message
    """
    try:
        profile = secure_profile_manager.get_profile(patient_id)
        if not profile:
            return {"error": "Patient profile not found"}
            
        if profile.auth_key not in ALLOWED_PATIENT_KEY:
            logging.warning(f"Security violation: {patient_id}")  # Audit Logging
            return {"error": "You do not have access!"}
            
        updated_profile = secure_profile_manager.update_profile(patient_id, updates)
        return updated_profile.to_dict()
        
    except Exception as e:
        return {"error": "Patient profile not found"}

