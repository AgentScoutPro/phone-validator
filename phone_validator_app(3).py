import streamlit as st
import pandas as pd
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

st.set_page_config(page_title="Phone Number Validator", page_icon="📱")

def validate_phone_number(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Basic validation
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        # Get additional information
        number_type = phonenumbers.number_type(parsed_number)
        is_mobile = number_type == phonenumbers.PhoneNumberType.MOBILE
        
        # Format number
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # Get carrier (if available)
        carrier_name = carrier.name_for_number(parsed_number, "en")
        
        # Get region/location
        location = geocoder.description_for_number(parsed_number, "en")
        
        # Get timezone
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        return {
            "formatted_number": formatted_number,
            "is_valid": is_valid,
            "is_possible": is_possible,
            "is_mobile": is_mobile,
            "carrier": carrier_name if carrier_name else "Unknown",
            "location": location if location else "Unknown",
            "timezone": ", ".join(time_zones) if time_zones else "Unknown"
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def main():
    st.title("📱 Phone Number Validator")
    st.write("Upload an Excel file with phone numbers or enter numbers manually to validate them.")
    
    tab1, tab2 = st.tabs(["File Upload", "Manual Entry"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                
                # Allow user to select the phone number column
                phone_column = st.selectbox("Select the phone number column:", df.columns)
                
                if st.button("Validate Numbers"):
                    results = []
                    progress_bar = st.progress(0)
                    
                    for index, row in df.iterrows():
                        phone = str(row[phone_column])
                        result = validate_phone_number(phone)
                        result['original_number'] = phone
                        results.append(result)
                        progress_bar.progress((index + 1) / len(df))
                    
                    results_df = pd.DataFrame(results)
                    st.write("Validation Results:")
                    st.dataframe(results_df)
                    
                    # Download button for results
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="phone_validation_results.csv",
                        mime="text/csv"
                    )
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab2:
        phone_input = st.text_input("Enter a phone number (with country code):", "+1234567890")
        
        if st.button("Validate"):
            if phone_input:
                result = validate_phone_number(phone_input)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.write("### Results")
                    st.write(f"Formatted Number: {result['formatted_number']}")
                    st.write(f"Valid: {'✅' if result['is_valid'] else '❌'}")
                    st.write(f"Mobile: {'✅' if result['is_mobile'] else '❌'}")
                    st.write(f"Carrier: {result['carrier']}")
                    st.write(f"Location: {result['location']}")
                    st.write(f"Timezone: {result['timezone']}")
            else:
                st.warning("Please enter a phone number")

if __name__ == "__main__":
    main()
