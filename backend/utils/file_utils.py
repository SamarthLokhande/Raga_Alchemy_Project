import os
import uuid
from werkzeug.utils import secure_filename
try:
    import magic
except ImportError:
    magic = None

class FileUtils:
    """Utilities for file handling and validation"""
    
    @staticmethod
    def allowed_file(filename, file_type='audio'):
        """Check if file extension is allowed"""
        if '.' not in filename:
            return False
            
        ext = filename.rsplit('.', 1)[1].lower()
        
        if file_type == 'audio':
            allowed_extensions = {'wav', 'mp3', 'ogg', 'flac'}
            return ext in allowed_extensions
        elif file_type == 'image':
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            return ext in allowed_extensions
        else:
            return False
    
    @staticmethod
    def validate_file_type(file_path, expected_type):
        """Validate file type using magic numbers"""
        try:
            if magic is None:
                return True  # Skip validation if magic is not available
                
            mime = magic.Magic(mime=True)
            file_mime = mime.from_file(file_path)
            
            if expected_type == 'audio':
                return file_mime.startswith('audio/')
            elif expected_type == 'image':
                return file_mime.startswith('image/')
            else:
                return True
        except:
            return True  # Fallback if magic is not available
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """Generate a unique filename"""
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_id = str(uuid.uuid4())
        
        if ext:
            return f"{unique_id}.{ext}"
        else:
            return unique_id
    
    @staticmethod
    def save_uploaded_file(file, upload_type='audio'):
        """Save uploaded file with validation"""
        try:
            # Validate filename
            if not FileUtils.allowed_file(file.filename, upload_type):
                raise ValueError(f"Invalid file type for {upload_type}")
            
            # Secure filename
            filename = secure_filename(file.filename)
            unique_filename = FileUtils.generate_unique_filename(filename)
            
            # Create upload directory
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            
            # Validate file content
            if not FileUtils.validate_file_type(file_path, upload_type):
                os.remove(file_path)
                raise ValueError("File content does not match expected type")
            
            return file_path
            
        except Exception as e:
            raise Exception(f"File upload failed: {str(e)}")
    
    @staticmethod
    def cleanup_file(file_path):
        """Safely remove a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except:
            pass
        return False