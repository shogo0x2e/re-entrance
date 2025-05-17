import { IsDate, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateClipDto {
  @IsDate()
  @Type(() => Date)
  recordedAt: Date;

  @IsInt()
  @Min(1)
  duration: number;
}
