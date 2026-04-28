from .patient_profiles import PatientProfileManager
from strands import tool
import logging
from typing import Dict, Optional, List

# Initialize the patient profile manager
profile_manager = PatientProfileManager()

@tool
def get_patient_profile(patient_id: str = None, email: str = None) -> Dict:
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
            profile = profile_manager.get_profile(patient_id)
        elif email:
            profile = profile_manager.get_profile_by_email(email)
        return profile.to_dict()
            
    except Exception as e:
            return {"error": "Patient profile not found"}
    
    


@tool
def get_patient_lab_results(patient_id: str = None, email: str = None) -> Dict:
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
            profile = profile_manager.get_profile(patient_id)
        elif email:
            profile = profile_manager.get_profile_by_email(email)
        return profile.lab_results   
    except Exception as e:
            return {"error": "Patient profile not found"}


@tool
def update_patient_profile(patient_id: str, updates: Dict) -> Dict:
    """
    Update patient profile information.
    
    Args:
        patient_id (str): The patient ID to update
        updates (dict): The updates to apply to the profile
        
    Returns:
        dict: Updated patient profile or error message
    """
    profile = profile_manager.update_profile(patient_id, updates)
    if not profile:
        return {"error": "Patient profile not found"}
        
    return profile.to_dict()
