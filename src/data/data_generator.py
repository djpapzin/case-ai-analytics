import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

def generate_synthetic_data(num_clients=1000, num_cases=5000, num_notes=10000):
    """
    Generate synthetic data for a legal case management system.
    
    Returns:
        clients_df: DataFrame with client information
        cases_df: DataFrame with case information
        case_notes_df: DataFrame with case notes
    """
    fake = Faker()
    
    # Set random seed for reproducibility
    np.random.seed(42)
    Faker.seed(42)
    
    # Generate Clients table
    clients = []
    for i in range(num_clients):
        clients.append({
            'client_id': i,
            'name': fake.name(),
            'age': np.random.randint(18, 80),
            'income_level': np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.5, 0.2]),
            'location': fake.city(),
            'join_date': fake.date_between(start_date='-5y', end_date='today')
        })
    clients_df = pd.DataFrame(clients)
    
    # Generate Cases table
    case_types = ['Family Law', 'Criminal Defense', 'Civil Litigation', 
                  'Corporate', 'Intellectual Property', 'Estate Planning']
    statuses = ['Resolved', 'Pending', 'Appealed', 'Abandoned']
    
    cases = []
    for i in range(num_cases):
        # Create realistic date relationships
        open_date = fake.date_between(start_date='-2y', end_date='today')
        open_date_dt = datetime.combine(open_date, datetime.min.time())
        
        # Some cases are still open
        is_resolved = np.random.random() < 0.7
        if is_resolved:
            # For resolved cases, calculate realistic resolution time (1 day to 1 year)
            resolution_days = np.random.randint(1, 365)
            resolution_date = open_date_dt + timedelta(days=resolution_days)
            status = np.random.choice(['Resolved', 'Appealed'], p=[0.9, 0.1])
        else:
            resolution_days = None
            resolution_date = None
            status = np.random.choice(['Pending', 'Abandoned'], p=[0.9, 0.1])
        
        case_type = np.random.choice(case_types, p=[0.25, 0.3, 0.2, 0.1, 0.1, 0.05])
        
        # Create realistic escalation patterns
        escalated = False
        if case_type in ['Criminal Defense', 'Civil Litigation']:
            escalated = np.random.random() < 0.3
        else:
            escalated = np.random.random() < 0.1
            
        assignee = f"Attorney_{np.random.randint(1, 20)}"
        
        cases.append({
            'case_id': i,
            'client_id': np.random.randint(0, num_clients),
            'case_type': case_type,
            'open_date': open_date,
            'close_date': resolution_date.date() if resolution_date else None,
            'resolution_days': resolution_days,
            'status': status,
            'complexity': np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.5, 0.2]),
            'assignee': assignee,
            'escalated': escalated
        })
    cases_df = pd.DataFrame(cases)
    
    # Generate Case Notes table
    note_types = ['Client Meeting', 'Document Review', 'Court Appearance', 
                  'Research', 'Client Communication', 'Internal Discussion']
    
    case_notes = []
    for i in range(num_notes):
        case_id = np.random.randint(0, num_cases)
        case_data = cases_df.loc[cases_df['case_id'] == case_id].iloc[0]
        
        # Create realistic note dates relative to case timeline
        if case_data['close_date'] is not None:
            note_date = fake.date_between(start_date=case_data['open_date'], 
                                          end_date=case_data['close_date'])
        else:
            note_date = fake.date_between(start_date=case_data['open_date'], 
                                          end_date='today')
        
        note_type = np.random.choice(note_types)
        
        # Generate realistic note text based on note type and case type
        if note_type == 'Client Meeting':
            note_text = f"Met with client to discuss {case_data['case_type']} case. {fake.paragraph()}"
        elif note_type == 'Court Appearance':
            note_text = f"Appeared in court for {fake.sentence()}. {fake.paragraph()}"
        else:
            note_text = fake.paragraph()
            
        case_notes.append({
            'note_id': i,
            'case_id': case_id,
            'note_date': note_date,
            'note_type': note_type,
            'note_text': note_text,
            'created_by': case_data['assignee'] if np.random.random() < 0.8 else f"Staff_{np.random.randint(1, 10)}"
        })
    case_notes_df = pd.DataFrame(case_notes)
    
    print(f"Generated {len(clients_df)} clients, {len(cases_df)} cases, and {len(case_notes_df)} case notes")
    
    return clients_df, cases_df, case_notes_df

if __name__ == "__main__":
    # Test data generation
    clients, cases, notes = generate_synthetic_data(100, 500, 1000)
    print(clients.head())
    print(cases.head())
    print(notes.head()) 