#!/usr/bin/env python3
"""
Update markdown files to use GCS URLs instead of local image paths.
Replaces local image references with GCS URLs.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class GCSURLUpdater:
    """Updates markdown files to use GCS URLs"""
    
    def __init__(self, base_dir: Path, bucket_name: str = "beginner-defi-concepts-gitbook-images"):
        self.base_dir = base_dir
        self.bucket_name = bucket_name
        self.gcs_base_url = f"https://storage.googleapis.com/{bucket_name}"
        self.lessons_dir = base_dir / 'content' / 'lessons'
    
    def update_lesson_file(self, lesson_file: Path, dry_run: bool = False) -> Dict:
        """Update a single lesson file"""
        if not lesson_file.exists():
            return {'error': f"File not found: {lesson_file}"}
        
        with open(lesson_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        replacements = []
        
        # Pattern to match local image references: ![alt](images/lessons/lesson_XX/filename.png)
        # Also match incorrectly formatted GCS URLs missing the lessons/ prefix
        local_pattern = re.compile(r'!\[([^\]]*)\]\(images/lessons/(lesson_\d+)/([^\)]+\.png)\)')
        gcs_pattern = re.compile(rf'!\[([^\]]*)\]\(https://storage\.googleapis\.com/{re.escape(self.bucket_name)}/(lesson_\d+)/([^\)]+\.png)\)')
        
        # First fix incorrectly formatted GCS URLs (missing lessons/ prefix)
        gcs_matches = list(gcs_pattern.finditer(content))
        for match in gcs_matches:
            alt_text = match.group(1)
            lesson_folder = match.group(2)
            filename = match.group(3)
            
            # Create correct GCS URL (structure: lessons/lesson_XX/filename.png)
            gcs_url = f"{self.gcs_base_url}/lessons/{lesson_folder}/{filename}"
            
            old_markdown = match.group(0)
            new_markdown = f"![{alt_text}]({gcs_url})"
            
            if old_markdown != new_markdown:
                replacements.append({
                    'old': old_markdown,
                    'new': new_markdown,
                    'filename': filename
                })
                content = content.replace(old_markdown, new_markdown)
        
        # Then handle local image references
        local_matches = list(local_pattern.finditer(content))
        for match in local_matches:
            alt_text = match.group(1)
            lesson_folder = match.group(2)
            filename = match.group(3)
            
            # Create GCS URL (structure: lessons/lesson_XX/filename.png)
            gcs_url = f"{self.gcs_base_url}/lessons/{lesson_folder}/{filename}"
            
            # Replace local path with GCS URL
            old_markdown = match.group(0)
            new_markdown = f"![{alt_text}]({gcs_url})"
            
            if old_markdown != new_markdown:
                replacements.append({
                    'old': old_markdown,
                    'new': new_markdown,
                    'filename': filename
                })
                content = content.replace(old_markdown, new_markdown)
        
        if replacements and not dry_run:
            with open(lesson_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            'file': str(lesson_file),
            'replacements': len(replacements),
            'details': replacements
        }
    
    def update_all(self, dry_run: bool = False) -> Dict:
        """Update all lesson files"""
        results = {
            'lessons': [],
            'total_replacements': 0
        }
        
        lesson_files = sorted(self.lessons_dir.glob("lesson-*.md"))
        
        print(f"\n{'='*60}")
        print(f"Updating {len(lesson_files)} lesson files to use GCS URLs")
        print(f"{'='*60}\n")
        
        for lesson_file in lesson_files:
            result = self.update_lesson_file(lesson_file, dry_run=dry_run)
            results['lessons'].append(result)
            results['total_replacements'] += result.get('replacements', 0)
            
            if result.get('replacements', 0) > 0:
                print(f"✓ {lesson_file.name}: {result['replacements']} images updated")
                if dry_run:
                    for rep in result.get('details', []):
                        print(f"    {rep['filename']}: {rep['old'][:50]}... → {rep['new'][:50]}...")
            else:
                print(f"⊘ {lesson_file.name}: No local image references found")
        
        print(f"\n{'='*60}")
        print(f"Summary: {results['total_replacements']} image references updated")
        print(f"{'='*60}\n")
        
        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update markdown files to use GCS URLs')
    parser.add_argument('--base-dir', type=str, help='Base directory of gitbook (default: parent of tools/)')
    parser.add_argument('--bucket', type=str, default='beginner-defi-concepts-gitbook-images', help='GCS bucket name')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    
    args = parser.parse_args()
    
    if args.base_dir:
        base_dir = Path(args.base_dir)
    else:
        base_dir = Path(__file__).parent.parent
    
    updater = GCSURLUpdater(base_dir, bucket_name=args.bucket)
    updater.update_all(dry_run=args.dry_run)

