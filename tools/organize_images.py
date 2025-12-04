#!/usr/bin/env python3
"""
Copy generated infographic images from assets/infographics/output to gitbook content/images directory
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List

class ImageOrganizer:
    """Organizes generated images into gitbook structure"""
    
    def __init__(self):
        """Initialize organizer with paths"""
        self.base_dir = Path(__file__).parent.parent
        self.source_dir = self.base_dir.parent.parent / 'assets' / 'infographics' / 'output' / 'beginner-defi-concepts'
        self.dest_dir = self.base_dir / 'content' / 'images' / 'lessons'
        self.specs_path = self.base_dir.parent.parent / 'assets' / 'infographics' / 'scripts' / 'beginner_defi_concepts_asset_specs.json'
        
        # Load specs
        with open(self.specs_path, 'r') as f:
            self.specs = json.load(f)
    
    def organize_lesson_images(self, lesson_id: str, dry_run: bool = False) -> Dict:
        """Copy images for a specific lesson"""
        lesson_data = self.specs.get('lessons', {}).get(lesson_id)
        if not lesson_data:
            return {'error': f"Lesson {lesson_id} not found"}
        
        lesson_num = int(lesson_id.replace('lesson_', ''))
        source_lesson_dir = self.source_dir / 'lessons' / lesson_id
        dest_lesson_dir = self.dest_dir / f"lesson_{lesson_num:02d}"
        
        if not source_lesson_dir.exists():
            return {'error': f"Source directory not found: {source_lesson_dir}"}
        
        dest_lesson_dir.mkdir(parents=True, exist_ok=True)
        
        results = {
            'lesson_id': lesson_id,
            'copied': [],
            'missing': [],
            'skipped': []
        }
        
        for asset in lesson_data['assets']:
            asset_id = asset['asset_id']
            asset_name = asset['title']
            
            # Find source file
            safe_name = asset_name.lower().replace(' ', '_').replace("'", '').replace(',', '')
            safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
            source_pattern = f"{asset_id}_*.png"
            
            source_files = list(source_lesson_dir.glob(source_pattern))
            if not source_files:
                results['missing'].append(asset_id)
                continue
            
            source_file = source_files[0]
            dest_file = dest_lesson_dir / source_file.name
            
            # Check if already exists and is same size
            if dest_file.exists() and dest_file.stat().st_size == source_file.stat().st_size:
                results['skipped'].append(asset_id)
                continue
            
            if not dry_run:
                shutil.copy2(source_file, dest_file)
                results['copied'].append(asset_id)
            else:
                results['copied'].append(asset_id)
        
        return results
    
    def organize_all(self, dry_run: bool = False) -> Dict:
        """Copy all images for all lessons"""
        print(f"\n{'='*60}")
        print("Organizing Beginner DeFi Concepts Images")
        print(f"{'='*60}\n")
        
        all_results = {
            'lessons': {},
            'total_copied': 0,
            'total_missing': 0,
            'total_skipped': 0
        }
        
        for lesson_id in sorted(self.specs.get('lessons', {}).keys()):
            print(f"Processing {lesson_id}...")
            result = self.organize_lesson_images(lesson_id, dry_run=dry_run)
            all_results['lessons'][lesson_id] = result
            
            if 'error' not in result:
                all_results['total_copied'] += len(result['copied'])
                all_results['total_missing'] += len(result['missing'])
                all_results['total_skipped'] += len(result['skipped'])
                
                if result['copied']:
                    print(f"  ✓ Copied: {len(result['copied'])} images")
                if result['missing']:
                    print(f"  ✗ Missing: {len(result['missing'])} images")
                if result['skipped']:
                    print(f"  ⊘ Skipped: {len(result['skipped'])} images (already exist)")
            else:
                print(f"  ✗ Error: {result['error']}")
        
        print(f"\n{'='*60}")
        print("Organization Complete!")
        print(f"{'='*60}")
        print(f"Total copied: {all_results['total_copied']}")
        print(f"Total missing: {all_results['total_missing']}")
        print(f"Total skipped: {all_results['total_skipped']}")
        print(f"{'='*60}\n")
        
        return all_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Organize generated images into gitbook structure')
    parser.add_argument('--lesson', help='Organize specific lesson (e.g., lesson_01)')
    parser.add_argument('--all', action='store_true', help='Organize all lessons')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without copying')
    
    args = parser.parse_args()
    
    organizer = ImageOrganizer()
    
    if args.all:
        organizer.organize_all(dry_run=args.dry_run)
    elif args.lesson:
        result = organizer.organize_lesson_images(args.lesson, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
    else:
        print("Usage:")
        print("  Organize all: python organize_images.py --all")
        print("  Organize lesson: python organize_images.py --lesson lesson_01")
        print("  Dry run: python organize_images.py --all --dry-run")

