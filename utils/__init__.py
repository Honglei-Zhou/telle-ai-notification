from .create_appt_intent import create_appt_intent
from .create_lead_inquiry import create_lead_inquiry
from .update_lead_intent import update_lead_intent
from .update_lead import update_lead

handler = {
    'UPDATE_LEAD_INTENT': update_lead_intent,
    'UPDATE_LEAD': update_lead,
    'CREATE_APPT_INTENT': create_appt_intent,
    'CREATE_LEAD_INQUIRY': create_lead_inquiry
}