#!/usr/bin/env python3
"""
TikTok Video Downloader Automation Script
Downloads TikTok videos in HD quality using tikdownloader.io
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin


class TikTokDownloader:
    def __init__(self):
        self.base_url = "https://tikdownloader.io"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def get_download_page(self, tiktok_url):
        """
        Submit TikTok URL to tikdownloader.io and get the download page
        """
        try:
            print(f"[*] Submitting TikTok URL: {tiktok_url}")
            
            # The API endpoint for tikdownloader.io
            api_url = f"{self.base_url}/api/ajaxSearch"
            
            # Update headers for API request
            self.session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': self.base_url,
                'Referer': f'{self.base_url}/en',
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            # Prepare the payload
            payload = {
                'q': tiktok_url,
                'lang': 'en'
            }
            
            print(f"[*] Sending POST request to API: {api_url}")
            response = self.session.post(api_url, data=payload)
            
            if response.status_code == 200:
                try:
                    # Try to parse as JSON first
                    json_data = response.json()
                    print(f"[*] Received JSON response")
                    return json_data
                except:
                    # If not JSON, return as text
                    print(f"[*] Received HTML response")
                    return response.text
            else:
                print(f"[!] Error: Received status code {response.status_code}")
                print(f"[*] Response: {response.text[:500]}")
                return None
                    
        except Exception as e:
            print(f"[!] Error getting download page: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def extract_hd_download_link(self, response_data):
        """
        Extract the HD download link from the response (JSON or HTML)
        """
        try:
            # If response is a dictionary (JSON), extract from there
            if isinstance(response_data, dict):
                print("[*] Parsing JSON response")
                
                # Check for status
                if response_data.get('status') == 'error':
                    error_msg = response_data.get('mess', 'Unknown error')
                    print(f"[!] API Error: {error_msg}")
                    return None
                
                # Look for download links in common JSON structures
                download_links = []
                
                # Method 1: Check for 'data' field with HTML content
                if 'data' in response_data:
                    html_content = response_data['data']
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Find all download links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        text = link.get_text().strip()
                        
                        # Look for HD or high quality downloads
                        if href.startswith('http') and any(keyword in text.lower() for keyword in ['hd', 'download', 'mp4', 'without watermark', 'no watermark']):
                            priority = 10 if 'hd' in text.lower() else 5
                            download_links.append({
                                'url': href,
                                'text': text,
                                'priority': priority
                            })
                
                # Method 2: Check for direct video URL fields
                possible_keys = ['url', 'video_url', 'download_url', 'hd_url', 'hdplay']
                for key in possible_keys:
                    if key in response_data and response_data[key]:
                        download_links.append({
                            'url': response_data[key],
                            'text': f'Direct link ({key})',
                            'priority': 9
                        })
                
                # Sort and return best option
                if download_links:
                    download_links.sort(key=lambda x: x['priority'], reverse=True)
                    print(f"[*] Found {len(download_links)} download options")
                    for i, link in enumerate(download_links[:3], 1):
                        url_preview = link['url'][:60] + '...' if len(link['url']) > 60 else link['url']
                        print(f"    {i}. {link['text']} - {url_preview}")
                    return download_links[0]['url']
                else:
                    print("[!] No download links found in JSON response")
                    print(f"[*] Response keys: {list(response_data.keys())}")
                    return None
            
            # If response is HTML string
            else:
                print("[*] Parsing HTML response")
                soup = BeautifulSoup(response_data, 'html.parser')
                
                # Look for download links - common patterns
                download_links = []
                
                # Method 1: Find links with "HD" or "Download" text
                for link in soup.find_all('a', href=True):
                    text = link.get_text().strip().lower()
                    href = link['href']
                    
                    if any(keyword in text for keyword in ['hd', 'download', 'mp4', 'without watermark']):
                        if href.startswith('http'):
                            download_links.append({
                                'url': href,
                                'text': link.get_text().strip(),
                                'priority': 10 if 'hd' in text else 5
                            })
                
                # Method 2: Look for download buttons
                download_buttons = soup.find_all(['a', 'button'], class_=re.compile(r'download|btn-download', re.I))
                for btn in download_buttons:
                    href = btn.get('href') or btn.get('data-href')
                    if href and href.startswith('http'):
                        download_links.append({
                            'url': href,
                            'text': btn.get_text().strip(),
                            'priority': 8
                        })
                
                # Method 3: Look for direct video links in the HTML
                video_tags = soup.find_all('video')
                for video in video_tags:
                    source = video.get('src') or (video.find('source') and video.find('source').get('src'))
                    if source and source.startswith('http'):
                        download_links.append({
                            'url': source,
                            'text': 'Direct Video Link',
                            'priority': 7
                        })
                
                # Sort by priority and return the best match
                if download_links:
                    download_links.sort(key=lambda x: x['priority'], reverse=True)
                    print(f"[*] Found {len(download_links)} download options")
                    for i, link in enumerate(download_links[:3], 1):
                        print(f"    {i}. {link['text']} ({link['url'][:50]}...)")
                    return download_links[0]['url']
                else:
                    print("[!] No download links found in the response")
                    # Print the HTML for debugging
                    print("[*] Response HTML (first 500 chars):")
                    print(str(response_data)[:500])
                    return None
                
        except Exception as e:
            print(f"[!] Error extracting download link: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def download_video(self, download_url, output_filename="tiktok_video.mp4"):
        """
        Download the video from the extracted URL
        """
        try:
            print(f"[*] Downloading video from: {download_url}")
            
            response = self.session.get(download_url, stream=True)
            
            if response.status_code == 200:
                # Get file size if available
                total_size = int(response.headers.get('content-length', 0))
                
                with open(output_filename, 'wb') as f:
                    if total_size:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress = (downloaded / total_size) * 100
                                print(f"\r[*] Download progress: {progress:.1f}%", end='', flush=True)
                        print()  # New line after progress
                    else:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                
                file_size = os.path.getsize(output_filename)
                print(f"[+] Video downloaded successfully: {output_filename} ({file_size / 1024 / 1024:.2f} MB)")
                return True
            else:
                print(f"[!] Failed to download video. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Error downloading video: {str(e)}")
            return False

    def download_tiktok_hd(self, tiktok_url, output_filename="tiktok_video.mp4"):
        """
        Main method to download TikTok video in HD
        """
        print(f"\n{'='*60}")
        print("TikTok HD Video Downloader")
        print(f"{'='*60}\n")
        
        # Step 1: Get the download page
        html_content = self.get_download_page(tiktok_url)
        if not html_content:
            print("[!] Failed to get download page")
            return False
        
        # Small delay to avoid rate limiting
        time.sleep(1)
        
        # Step 2: Extract HD download link
        download_url = self.extract_hd_download_link(html_content)
        if not download_url:
            print("[!] Failed to extract download link")
            return False
        
        # Step 3: Download the video
        success = self.download_video(download_url, output_filename)
        
        if success:
            print(f"\n[+] Download completed successfully!")
            print(f"[+] Video saved as: {output_filename}")
        else:
            print(f"\n[!] Download failed!")
        
        return success


def main():
    """
    Main function - example usage
    """
    # Example TikTok URL - replace with your actual TikTok video URL
    tiktok_url = input("Enter TikTok video URL: ").strip()
    
    if not tiktok_url:
        print("[!] Please provide a valid TikTok URL")
        return
    
    # Optionally specify output filename
    output_filename = input("Enter output filename (press Enter for default 'tiktok_video.mp4'): ").strip()
    if not output_filename:
        output_filename = "tiktok_video.mp4"
    
    # Ensure .mp4 extension
    if not output_filename.endswith('.mp4'):
        output_filename += '.mp4'
    
    # Create downloader instance and download
    downloader = TikTokDownloader()
    downloader.download_tiktok_hd(tiktok_url, output_filename)


if __name__ == "__main__":
    main()
