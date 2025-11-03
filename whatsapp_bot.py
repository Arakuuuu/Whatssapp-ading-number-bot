import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WhatsAppBot:
    def __init__(self):
        """Initialize the WhatsApp bot with Chrome driver"""
        print("Starting WhatsApp Bot...")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        
    def login(self):
        """Open WhatsApp Web and wait for QR code scan"""
        print("\n[1/4] Opening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        print("📱 Please scan the QR code with your phone")
        
        # Wait for login
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            print("✓ Login successful!\n")
            time.sleep(2)
            return True
        except TimeoutException:
            print("✗ Login timeout. Please try again.")
            return False
    
    def verify_group(self, group_name):
        """Search and verify if group exists"""
        print(f"[2/4] Verifying group: '{group_name}'")
        
        try:
            # Clear any previous search
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            search_box.click()
            search_box.clear()
            time.sleep(1)
            
            # Search for group
            search_box.send_keys(group_name)
            time.sleep(2)
            
            # Try to find and click the group
            group = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f'//span[@title="{group_name}"]')
            ))
            group.click()
            print(f"✓ Group found and opened!\n")
            time.sleep(2)
            return True
            
        except TimeoutException:
            print(f"✗ Group '{group_name}' not found. Please check the name and try again.\n")
            return False
    
    def clean_phone_number(self, number):
        """Clean phone number by removing spaces and special characters"""
        # Remove everything except digits and +
        cleaned = re.sub(r'[^\d+]', '', number.strip())
        # Remove + if present
        cleaned = cleaned.replace('+', '')
        return cleaned
    
    def add_single_member(self, phone_number):
        """Add a single member to the group"""
        try:
            # Click group menu
            menu = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@aria-label="Menu"]')
            ))
            menu.click()
            time.sleep(1)
            
            # Click "Group info"
            group_info = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[contains(text(), "Group info") or contains(text(), "Informations du groupe")]')
            ))
            group_info.click()
            time.sleep(2)
            
            # Click "Add participant"
            add_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@aria-label="Add participants" or @aria-label="Ajouter des participants"]')
            ))
            add_btn.click()
            time.sleep(2)
            
            # Enter phone number
            search_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            search_input.clear()
            search_input.send_keys(phone_number)
            time.sleep(3)
            
            # Select contact
            contact = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@role="listitem"]')
            ))
            contact.click()
            time.sleep(1)
            
            # Click add/confirm button
            confirm = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@aria-label="Add" or @aria-label="Ajouter"]')
            ))
            confirm.click()
            time.sleep(2)
            
            # Go back to chat (click back twice)
            back = self.driver.find_element(By.XPATH, '//button[@aria-label="Back" or @aria-label="Retour"]')
            back.click()
            time.sleep(1)
            back = self.driver.find_element(By.XPATH, '//button[@aria-label="Back" or @aria-label="Retour"]')
            back.click()
            time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"  Error details: {str(e)[:50]}")
            # Try to go back if stuck
            try:
                backs = self.driver.find_elements(By.XPATH, '//button[@aria-label="Back" or @aria-label="Retour"]')
                for back in backs:
                    back.click()
                    time.sleep(0.5)
            except:
                pass
            return False
    
    def add_members(self, phone_numbers):
        """Add multiple members to the group"""
        print(f"[4/4] Adding {len(phone_numbers)} members to group...\n")
        
        success_count = 0
        failed_numbers = []
        
        for idx, number in enumerate(phone_numbers, 1):
            print(f"[{idx}/{len(phone_numbers)}] Adding {number}...", end=" ")
            
            if self.add_single_member(number):
                print("✓")
                success_count += 1
            else:
                print("✗")
                failed_numbers.append(number)
            
            # Small delay between additions
            time.sleep(2)
        
        # Summary
        print(f"\n{'='*50}")
        print(f"SUMMARY:")
        print(f"  Successfully added: {success_count}/{len(phone_numbers)}")
        print(f"  Failed: {len(failed_numbers)}/{len(phone_numbers)}")
        if failed_numbers:
            print(f"\nFailed numbers:")
            for num in failed_numbers:
                print(f"  - {num}")
        print(f"{'='*50}\n")
    
    def close(self):
        """Close the browser"""
        print("Closing browser...")
        self.driver.quit()


def get_phone_numbers():
    """Get list of phone numbers from user input"""
    print("[3/4] Enter phone numbers (one per line)")
    print("Accepted formats: +221 77 887 80 24 or 221778878024")
    print("Press Enter twice when done:\n")
    
    numbers = []
    while True:
        line = input().strip()
        if not line:
            break
        numbers.append(line)
    
    return numbers


def main():
    print("="*50)
    print("WhatsApp Group Member Adder Bot")
    print("="*50)
    
    bot = WhatsAppBot()
    
    try:
        # Step 1: Login
        if not bot.login():
            return
        
        # Step 2: Get and verify group
        while True:
            group_name = input("Enter the group name (exactly as it appears): ").strip()
            if bot.verify_group(group_name):
                break
            retry = input("Try again? (y/n): ").lower()
            if retry != 'y':
                return
        
        # Step 3: Get phone numbers
        raw_numbers = get_phone_numbers()
        
        if not raw_numbers:
            print("No numbers provided. Exiting...")
            return
        
        # Clean phone numbers
        cleaned_numbers = [bot.clean_phone_number(num) for num in raw_numbers]
        print(f"\nCleaned {len(cleaned_numbers)} numbers")
        
        # Confirm before adding
        print(f"\nReady to add {len(cleaned_numbers)} members to '{group_name}'")
        confirm = input("Continue? (y/n): ").lower()
        
        if confirm == 'y':
            # Step 4: Add members
            bot.add_members(cleaned_numbers)
            print("\n✓ Process completed!")
        else:
            print("Cancelled by user")
        
        # Keep browser open
        input("\nPress Enter to close the browser...")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
