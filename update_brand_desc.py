from app import create_app, db
from app.models import BrandInfo

# 브랜드 설명을 수정하려면 아래 리스트에 원하는 브랜드명과 설명을 추가
# 예시: ("Fender", "내가 원하는 설명")
updates = [
    ("Fender", "내가 원하는 설명"),
    ("Gibson", "깊고 따뜻한 사운드, 새로운 설명"),
    # ("수정할 브랜드명", "설명")
]

def update_brand_descriptions():
    app = create_app()
    with app.app_context():
        for name, desc in updates:
            brand = BrandInfo.query.filter_by(name=name).first()
            if brand:
                brand.description = desc
                print(f"{name} 설명 수정 완료!")
            else:
                print(f"{name} 브랜드를 찾을 수 없습니다.")
        db.session.commit()
        print("모든 변경사항이 저장되었습니다.")

if __name__ == "__main__":
    update_brand_descriptions()
