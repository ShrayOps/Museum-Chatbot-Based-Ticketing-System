import mysql.connector
import uuid
from datetime import datetime

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'museum_chatbot'
}

def get_db_connection():
    """Establish and return a database connection"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def initialize_db():
    """Initialize database tables if they don't exist"""
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Create bookings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id VARCHAR(36) PRIMARY KEY,
        booking_date DATE NOT NULL,
        num_tickets INT NOT NULL,
        ticket_type VARCHAR(20) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create chat_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        language VARCHAR(10) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def save_booking(booking_date, num_tickets, ticket_type, price):
    """Save booking information and return booking ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    
    # Generate unique booking ID
    booking_id = str(uuid.uuid4())
    
    # Convert string date to MySQL date format
    formatted_date = datetime.strptime(booking_date, '%d/%m/%Y').strftime('%Y-%m-%d')
    
    # Insert booking record
    query = '''
    INSERT INTO bookings (id, booking_date, num_tickets, ticket_type, price)
    VALUES (%s, %s, %s, %s, %s)
    '''
    
    cursor.execute(query, (booking_id, formatted_date, num_tickets, ticket_type, price))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return booking_id

def check_availability(booking_date, num_tickets, ticket_type):
    """Check if tickets are available for the specified date"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Convert string date to MySQL date format
    formatted_date = datetime.strptime(booking_date, '%d/%m/%Y').strftime('%Y-%m-%d')
    
    # Get total booked tickets for the day
    query = '''
    SELECT SUM(num_tickets) FROM bookings 
    WHERE booking_date = %s AND ticket_type = %s
    '''
    
    cursor.execute(query, (formatted_date, ticket_type))
    result = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    # Assuming max capacity is 500 tickets per day
    max_capacity = 500
    booked = result if result else 0
    
    return (booked + num_tickets) <= max_capacity

def save_chat_log(user_message, bot_response, language):
    """Save chat interaction to the database"""
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    query = '''
    INSERT INTO chat_logs (user_message, bot_response, language)
    VALUES (%s, %s, %s)
    '''
    
    cursor.execute(query, (user_message, bot_response, language))
    conn.commit()
    
    cursor.close()
    conn.close()

def get_analytics():
    """Retrieve analytics data for dashboard"""
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    # Get total bookings
    cursor.execute("SELECT COUNT(*) as total_bookings FROM bookings")
    total_bookings = cursor.fetchone()['total_bookings']
    
    # Get revenue
    cursor.execute("SELECT SUM(price) as total_revenue FROM bookings")
    total_revenue = cursor.fetchone()['total_revenue'] or 0
    
    # Get bookings by type
    cursor.execute("""
    SELECT ticket_type, COUNT(*) as count 
    FROM bookings 
    GROUP BY ticket_type
    """)
    bookings_by_type = cursor.fetchall()
    
    # Get most popular dates
    cursor.execute("""
    SELECT booking_date, SUM(num_tickets) as tickets_sold
    FROM bookings
    GROUP BY booking_date
    ORDER BY tickets_sold DESC
    LIMIT 5
    """)
    popular_dates = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'bookings_by_type': bookings_by_type,
        'popular_dates': popular_dates
    }
